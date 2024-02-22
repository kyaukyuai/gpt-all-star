# gpt_all_star/helper/pull_request.py

from gpt_all_star.helper.git import Git


class PullRequest:
    def __init__(self, git: Git):
        self.git = git

    def create_pull_request(self, branch_name: str) -> None:
        try:
            self.git.create_pull_request(
                title=branch_name,
                body="",
                head=branch_name,
                base="main",
            )
            print("Pull request has been created.")
        except Exception as e:
            print(f"Error creating pull request: {e}")
