import os
from pathlib import Path

import git
import requests
from github import Github


class Git:
    def __init__(self, repo_path: Path) -> None:
        self._create_new_github_repository(repo_path.name)
        self.repo_path = repo_path
        self.repo = git.Repo.init(self.repo_path)
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.github_repo = self.github.get_repo(
            f"{os.getenv('GITHUB_ORG')}/{repo_path.name}"
        )

    def url(self):
        return f"https://github.com/{os.getenv('GITHUB_ORG')}/{self.repo_path.name}"

    def files(self):
        excluded_dirs = ["node_modules", ".git", ".archive", ".idea", "build"]
        return [
            str(file)
            for file in self.repo_path.rglob("*")
            if file.is_file()
            and not any(excluded_dir in str(file) for excluded_dir in excluded_dirs)
        ]

    def diffs(self):
        try:
            if self.repo.head.is_valid() and list(self.repo.iter_commits()):
                staged_diffs = self.repo.git.diff("HEAD")
                not_staged_diffs = self.repo.git.diff()
                return staged_diffs + "\n" + not_staged_diffs
            else:
                return "No commits in the repository."
        except git.exc.GitCommandError as e:
            return f"An error occurred while executing git command.: {e}"

    def checkout(self, branch_name):
        try:
            self.repo.git.checkout("HEAD", b=branch_name)
            return True
        except git.exc.GitCommandError as e:
            print(f"Error creating new branch: {e}")
            return False

    def add(self, files):
        self.repo.index.add(files)

    def commit(self, commit_message: str = "Add files via gpt-all-star"):
        self.repo.index.commit(commit_message)

    def push(self):
        try:
            remote_name = "origin"
            remote_url = f"https://github.com/{os.getenv('GITHUB_ORG')}/{self.repo_path.name}.git"
            if remote_name in self.repo.remotes:
                remote = self.repo.remotes[remote_name]
                if remote.url != remote_url:
                    remote.set_url(remote_url)
            else:
                remote = self.repo.create_remote(remote_name, remote_url)

            current_branch = self.repo.active_branch.name
            remote.push(refspec=f"{current_branch}:{current_branch}")
            print("Push successful!")
        except git.exc.GitCommandError as e:
            print(f"Failed to push to the repository: {e}")
            raise e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e

    def create_pull_request(self, branch_name):
        try:
            self.github_repo.create_pull(
                title=branch_name,
                body="",
                head=branch_name,
                base="main",
            )
            print("Pull request has been created.")
        except Exception as e:
            print(f"Error creating pull request: {e}")

    def check_local_main_branch_exists(self) -> bool:
        return any(head.name == "main" for head in self.repo.heads)

    def check_github_main_branch_exists(self) -> bool:
        branches = self.github_repo.get_branches()
        return any(branch.name == "main" for branch in branches)

    def _create_new_github_repository(self, repository_name) -> None:
        url = f"https://api.github.com/orgs/{os.getenv('GITHUB_ORG')}/repos"
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
