from ast import Dict
import uuid

import requests

from core.config import settings

uuid_str = str(uuid.uuid4())

print(uuid_str)


def get_access_token(client_id: str, client_secret: str) -> str:
    url = "https://api.getport.io/v1/auth/access_token"
    headers = {"Content-Type": "application/json"}
    data = {
        "clientId": client_id,
        "clientSecret": client_secret,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["accessToken"]


def create_django_service(access_token: str, blueprint_id: str, properties) -> None:
    url = f"https://api.getport.io/v1/blueprints/{blueprint_id}/actions/CreateDjangoService/runs"
    headers = {"Authorization": f"Bearer {access_token}",
               "Content-Type": "application/json"}
    data = {"properties": properties}
    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    response.raise_for_status()


token = get_access_token(settings.PORT_CLIENT_ID, settings.PORT_CLIENT_SECRET)
create_django_service(token, settings.PORT_SERVICE_BLUEPRINT,  {
                      "repository_name": uuid_str, "project_name": uuid_str, "description": "some desc"})
