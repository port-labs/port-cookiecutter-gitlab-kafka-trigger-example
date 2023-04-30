from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "port-cookiecutter-gitlab-example"

    PORT_API_URL: str = "https://api.getport.io/v1"
    PORT_SERVICE_BLUEPRINT: str = "microservice"
    PORT_CLIENT_ID: str
    PORT_CLIENT_SECRET: str

    GITLAB_ACCESS_TOKEN: str
    GITLAB_DOMAIN: str = "gitlab.com"
    GITLAB_GROUP_NAME: str

    COOKIECUTTER_DJANGO_URL: str = "https://github.com/cookiecutter/cookiecutter-django"
    COOKIECUTTER_GO_URL: str = "https://github.com/lacion/cookiecutter-golang"
    COOKIECUTTER_CPP_URL: str = "https://github.com/DerThorsten/cpp_cookiecutter"
    COOKIECUTTER_OUTPUT_DIR: str = "cookiecutter_output/{uuid}"

    KAFKA_USER: str
    KAFKA_PASSWORD: str
    KAFKA_BOOTSTRAP_SERVERS: str = "b-1-public.publicclusterprod.t9rw6w.c1.kafka.eu-west-1.amazonaws.com: 9196, b-2-public.publicclusterprod.t9rw6w.c1.kafka.eu-west-1.amazonaws.com: 9196, b-3-public.publicclusterprod.t9rw6w.c1.kafka.eu-west-1.amazonaws.com: 9196"
    KAFKA_RUNS_TOPIC: str
    KAFKA_CONSUMER_AUTO_OFFSET_RESET: str = "earliest"


class Config:
    case_sensitive = True


settings = Settings()
