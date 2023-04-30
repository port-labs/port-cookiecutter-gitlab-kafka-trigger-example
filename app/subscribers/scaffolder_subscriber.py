import logging

from kafka.consumer import KafkaConsumer
from mappings import ACTION_ID_TO_CLASS_MAPPING
from clients import port
from core.config import settings
from schemas.data import Data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start() -> None:
    logger.info("Starting Scaffolder Subscriber")
    consumer = KafkaConsumer(msg_process=handle_create_service)

    consumer.start()


def handle_create_service(data: Data):
    logger.info(f"data body: {data}")

    port.add_action_log_message(
        data['context']['runId'], "Got message, starting to process 🏃")
    action_type = data['payload']['action']['trigger']
    action_identifier = data['payload']['action']['identifier']
    properties = data['payload']['properties']
    repo = properties.pop('repository_name')
    run_id = data['context']['runId']

    if action_type == 'CREATE':
        port.add_action_log_message(
            data['context']['runId'], f"{action_identifier} - creating a new service is GitLab 😼")
        logger.info(f"{action_identifier} - create new service")
        action_status = ACTION_ID_TO_CLASS_MAPPING.get(
            action_identifier)().create(repo, properties)
        message = f"{action_identifier} - action status after creating service is {action_status}"

        if action_status == 'SUCCESS':
            port.add_action_log_message(
                data['context']['runId'], f"{action_identifier} - action status after creating service is {action_status} ✅")

            entity_properties = {
                'description': next(iter([value for key, value in properties.items() if 'description' in key.lower()]),
                                    ''),
                'url': f"https://{settings.GITLAB_DOMAIN}/{settings.GITLAB_GROUP_NAME}/{repo}"
            }
            port.add_action_log_message(
                data['context']['runId'], f"Creating a new entity in Port 🚢")

            create_status = port.create_entity(blueprint=settings.PORT_SERVICE_BLUEPRINT,
                                               title=f"{settings.GITLAB_GROUP_NAME}/{repo}",
                                               properties=entity_properties, run_id=run_id)
            action_status = 'SUCCESS' if 200 <= create_status <= 299 else 'FAILURE'
            message = f"{message}, after creating entity is {action_status}"
        else:
            port.add_action_log_message(
                data['context']['runId'], f"{action_identifier} - action status after creating service is {action_status} ❌")

        port.update_action(run_id, message, action_status)
        return {'status': 'SUCCESS'}

    return {'status': 'IGNORED'}
