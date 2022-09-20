import logging
import git
import shutil
from typing import Literal, Union

from clients import git, github

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseCreateService:

    def create(self, github_org: str, github_repo: str, props: dict) -> Union[Literal['FAILURE'], Literal['SUCCESS']]:
        project_dir = None
        try:
            project_dir = self._create_cookiecutter(props)
            github.create_repo(github_org, github_repo)
            repo = git.init_repo(project_dir)
            git.upload_all_files(repo, github_org, github_repo)
            logger.info(f"{self.__class__.__name__} - success")
            return 'SUCCESS'
        except Exception as err:
            logger.error(f"{self.__class__.__name__} - error: {err}")
        finally:
            if project_dir:
                shutil.rmtree(project_dir)

        return 'FAILURE'

    def _create_cookiecutter(self, props: dict):
        raise NotImplementedError("Subclasses should implement '_create_cookiecutter'")
