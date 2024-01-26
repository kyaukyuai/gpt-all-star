import os
from pathlib import Path
import git
import requests


class Git:
    def __init__(self, repo_path: Path) -> None:
        self._create_new_github_repository(repo_path.name)
        self.repo_path = repo_path
        self.repo = git.Repo.init(self.repo_path)

    def files(self):
        return [
            str(file)
            for file in self.repo_path.rglob("*")
            if file.is_file()
            and "node_modules" not in str(file)
            and ".git" not in str(file)
            and ".archive" not in str(file)
        ]

    def diffs(self):
        try:
            if self.repo.head.is_valid() and list(self.repo.iter_commits()):
                return self.repo.git.diff("HEAD")
            else:
                return "No commits in the repository."
        except git.exc.GitCommandError:
            return "An error occurred while executing git command."

    def add(self, files):
        self.repo.index.add(files)

    def commit(self, commit_message: str = "Add files via gpt-all-star"):
        self.repo.index.commit(commit_message)

    def push(self):
        try:
            remote_name = "origin"
            remote_url = f"https://github.com/gpt-all-star/{self.repo_path.name}.git"
            if remote_name in self.repo.remotes:
                remote = self.repo.remotes[remote_name]
                if remote.url != remote_url:
                    remote.set_url(remote_url)
            else:
                remote = self.repo.create_remote(remote_name, remote_url)

            current_branch = self.repo.active_branch.name
            remote.push(refspec=f"{current_branch}:{current_branch}")
        except git.exc.GitCommandError as e:
            print(f"Failed to push to the repository: {e}")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e

    def _create_new_github_repository(self, repository_name) -> None:
        url = "https://api.github.com/orgs/gpt-all-star/repos"
        token = os.getenv("GITHUB_TOKEN")

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        data = {"name": repository_name, "private": False}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            if any(repo["name"] == repository_name for repo in repos):
                print("Repository already exists, skipping creation.")
                return

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            print("Repository created successfully.")
        else:
            print(
                f"Failed to create repository. Status code: {response.status_code}, {response.text}"
            )
