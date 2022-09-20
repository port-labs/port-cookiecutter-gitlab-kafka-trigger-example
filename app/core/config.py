from pydantic import BaseSettings


class Settings(BaseSettings):
    API_STR: str = "/api"
    PROJECT_NAME: str = "port-cookiecutter-example"

    PORT_API_URL: str = "https://api.getport.io/v1"
    PORT_SERVICE_BLUEPRINT: str = "service"
    PORT_CLIENT_ID: str
    PORT_CLIENT_SECRET: str

    GH_ACCESS_TOKEN: str

    COOKIECUTTER_DJANGO_URL: str = "https://github.com/cookiecutter/cookiecutter-django"
    COOKIECUTTER_GO_URL: str = "https://github.com/lacion/cookiecutter-golang"
    COOKIECUTTER_CPP_URL: str = "https://github.com/DerThorsten/cpp_cookiecutter"
    COOKIECUTTER_OUTPUT_DIR: str = "cookiecutter_output/{uuid}"

    class Config:
        case_sensitive = True


settings = Settings()
