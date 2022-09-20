from github import Github

from core.config import settings

g = Github(settings.GH_ACCESS_TOKEN)


def create_repo(github_org: str, github_repo: str):
    org = g.get_organization(github_org)
    org.create_repo(github_repo, private=True)
