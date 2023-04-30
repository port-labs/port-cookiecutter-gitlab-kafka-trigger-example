<img align="right" src="https://user-images.githubusercontent.com/8277210/183290078-f38cdfd2-e5da-4562-82e6-f274d0330825.svg#gh-dark-mode-only" width="100" height="74" /> <img align="right" width="100" height="74" src="https://user-images.githubusercontent.com/8277210/183290025-d7b24277-dfb4-4ce1-bece-7fe0ecd5efd4.svg#gh-light-mode-only" />

# port-cookiecutter-gitlab-kafka-trigger-example

[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://join.slack.com/t/devex-community/shared_invite/zt-1bmf5621e-GGfuJdMPK2D8UN58qL4E_g)

Port is the Developer Platform meant to supercharge your DevOps and Developers, and allow you to regain control of your environment.


## Description

The following example creates service GitHub repository from Cookiecutter repository.

This example consists of a Kafka consumer backend, that listen for Port Action events.

For each event, the backend creates new project using Cookiecutter, and new GitHub repository to host the project.

Finally, the backend creates new Port Entity for `microservice` blueprint, and updates Port Action run.

### Docker

1. Make sure that the Docker daemon is available and running
```
$ docker info
```

2. Create `.env` file with the required environment variables
```
$ cat .env

PORT_CLIENT_ID=<PORT_CLIENT_ID>
PORT_CLIENT_SECRET=<PORT_CLIENT_SECRET>
GITLAB_ACCESS_TOKEN=<GITLAB_ACCESS_TOKEN>
gitlab.com=<For example gitlab.com>
GITLAB_GROUP_NAME=<YOUR_GROUP>
KAFKA_USER=<YOUR_USERNAME>
KAFKA_PASSWORD=<YOUR_PASSWORD>
KAFKA_RUNS_TOPIC=<YOUR_TOPIC>
```

Make sure your `GITLAB_ACCESS_TOKEN` has relevant scopes for create new repository in your organization, and push to it.

![image](https://user-images.githubusercontent.com/51213812/233837042-afda1f2b-5fb6-4e86-8469-9b78552ff1c7.png)


3. Build example's Docker image
```
$ docker build -t getport.io/port-cookiecutter-gitlab-kafka-trigger-example .
```

4. Run example's Docker image with `.env`

To change the default port (`80`) to `8080` for example, replace command's flags with the following: `-p 80:8080 -e PORT="8080"`
```
$ docker run -d --name getport.io-port-cookiecutter-gitlab-kafka-trigger-example --env-file .env getport.io/port-cookiecutter-gitlab-kafka-trigger-example
```

5. Verify that the Docker container is up and running, and ready to listen for new webhooks:
```
$ docker logs -f getport.io-port-cookiecutter-gitlab-kafka-trigger-example
```
```
...
INFO:subscribers.scaffolder_subscriber:Starting Scaffolder Subscriber
INFO:kafka.consumer:Assignment: [TopicPartition{topic=org_yWVmPI3kZZgxNBvj.runs,partition=0,offset=-1001,leader_epoch=None,error=None}]
...
```

```
`docker logs -f` command follows log output, and helps you also to troubleshoot future action runs.
```

### Port

1. Create `microservice` blueprint:
```
{
    "identifier": "microservice",
    "title": "Microservice",
    "icon": "Service",
    "schema": {
        "properties": {
            "description": {
                "type": "string",
                "title": "Description"
            },
            "url": {
                "type": "string",
                "format": "url",
                "title": "URL"
            }
        },
        "required": []
    },
    "mirrorProperties": {},
    "calculationProperties": {}
}
```

2. Create new actions for blueprint:

```
[
    {
        "identifier": "CreateDjangoService",
        "title": "Create Django",
        "icon": "Service",
        "userInputs": {
            "properties": {
                "repository_name": {
                    "type": "string"
                },
                "project_name": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            },
            "required": [
                "repository_name"
            ]
        },
        "invocationMethod": {
            "type": "KAFKA"
        },
        "trigger": "CREATE",
        "description": "Creates a new Django service"
    },
    {
        "identifier": "CreateCPPService",
        "title": "Create C++",
        "icon": "Service",
        "userInputs": {
            "properties": {
                "repository_name": {
                    "type": "string"
                },
                "project_name": {
                    "type": "string"
                },
                "description": {
                    "type": "string"
                }
            },
            "required": [
                "repository_name"
            ]
        },
        "invocationMethod": {
            "type": "KAFKA"
        },
        "trigger": "CREATE",
        "description": "Creates a new C++ service"
    },
    {
        "identifier": "CreateGoService",
        "title": "Create Go",
        "icon": "Service",
        "userInputs": {
            "properties": {
                "repository_name": {
                    "type": "string"
                },
                "app_name": {
                    "type": "string"
                },
                "project_short_description": {
                    "type": "string"
                }
            },
            "required": [
                "repository_name"
            ]
        },
        "invocationMethod": {
            "type": "KAFKA"
        },
        "trigger": "CREATE",
        "description": "Creates a new Go service"
    }
]
```

3. Run the action with some input (replace `<OUTPUT_GITLAB_REPO>`):
```
{
  "repository_name": "<OUTPUT_GITLAB_REPO>",
  "project_name": "new-django-service",
  "description": "New Django Service"
}
```

4. Verify status and outcome of the action run in Port (run status in audit logs, new entities, ...).
