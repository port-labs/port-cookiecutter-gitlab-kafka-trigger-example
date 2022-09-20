from cookiecutter.main import cookiecutter

from actions.base_create_service import BaseCreateService
from utils import get_unique_output_dir
from core.config import settings


class CreateDjangoService(BaseCreateService):

    def _create_cookiecutter(self, props: dict):
        return cookiecutter(settings.COOKIECUTTER_DJANGO_URL, extra_context=props,
                            no_input=True, output_dir=get_unique_output_dir())
