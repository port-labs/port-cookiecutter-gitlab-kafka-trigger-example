import logging
import json
import requests
from typing import Literal, Union

from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_port_api_token():
    """
    Get a Port API access token
    This function uses CLIENT_ID and CLIENT_SECRET from config
    """

    credentials = {'clientId': settings.PORT_CLIENT_ID,
                   'clientSecret': settings.PORT_CLIENT_SECRET}

    token_response = requests.post(
        f"{settings.PORT_API_URL}/auth/access_token", json=credentials)

    return token_response.json()['accessToken']


def create_entity(blueprint: str, title: str, properties: dict, run_id: str, identifier: str = None):
    """
    Create new entity for blueprint in Port
    """

    token = get_port_api_token()
    headers = {
        'Authorization': f"Bearer {token}"
    }
    body = {
        "title": title,
        "properties": properties
    }

    if identifier:
        body['identifier'] = identifier

    logger.info(f"create entity with: {json.dumps(body)}")
    response = requests.post(f"{settings.PORT_API_URL}/blueprints/{blueprint}/entities?run_id={run_id}",
                             json=body, headers=headers)
    logger.info(
        f"create entity response - status: {response.status_code}, body: {json.dumps(response.json())}")

    return response.status_code


def update_action(run_id: str, message: str, status: Union[Literal['FAILURE'], Literal['SUCCESS']]):
    """
    Reports to Port on the status of an action run
    """

    token = get_port_api_token()
    headers = {
        'Authorization': f"Bearer {token}"
    }
    body = {
        'status': status,
        'message': {
            'message': message
        }
    }

    logger.info(f"update action with: {json.dumps(body)}")
    response = requests.patch(
        f"{settings.PORT_API_URL}/actions/runs/{run_id}", json=body, headers=headers)
    logger.info(
        f"update action response - status: {response.status_code}, body: {json.dumps(response.json())}")

    return response.status_code


def add_action_log_message(run_id: str, message: str):
    '''
    Adds a new log line to the specified Port self-service action run
    '''
    token = get_port_api_token()

    headers = {
        'Authorization': f"Bearer {token}"
    }
    body = {
        "message": message
    }

    response = requests.post(
        f"{settings.PORT_API_URL}/actions/runs/{run_id}/logs", json=body, headers=headers)
    if response.status_code != 200 and response.status_code != 201:
        logger.error('Failed to add log line to run ID')
        logger.error(f'Desired message: {message}')
        logger.error(json.dumps(response.json()))
    else:
        logger.debug('Added new log line to action')

    return response.status_code
