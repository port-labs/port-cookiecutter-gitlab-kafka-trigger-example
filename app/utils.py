import uuid

from core.config import settings


def get_unique_output_dir():
    return settings.COOKIECUTTER_OUTPUT_DIR.format(uuid=uuid.uuid4().hex)
