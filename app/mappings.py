from typing import Dict, Type

from actions.base_create_service import BaseCreateService
from actions.create_cpp_service import CreateCPPService
from actions.create_django_service import CreateDjangoService
from actions.create_go_service import CreateGoService

ACTION_ID_TO_CLASS_MAPPING: Dict[str, Type[BaseCreateService]] = {
    "CreateDjangoService": CreateDjangoService,
    "CreateGoService": CreateGoService,
    "CreateCPPService": CreateCPPService
}
