from git import Repo

from core.config import settings

remote_name = "origin"


def init_repo(path):
    return Repo.init(path)


def upload_all_files(repo: Repo, remote_org: str, remote_repo: str, commit_msg="Initial Commit", head_branch="main"):
    repo.git.add('.')
    repo.index.commit(commit_msg)
    remote_url = f"https://{settings.GH_ACCESS_TOKEN}@github.com/{remote_org}/{remote_repo}"
    repo.create_remote(name=remote_name, url=remote_url)
    branch = repo.create_head(head_branch)
    repo.git.push("--set-upstream", remote_name, branch)
