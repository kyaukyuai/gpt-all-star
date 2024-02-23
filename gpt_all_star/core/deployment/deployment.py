from rich.syntax import Syntax

from gpt_all_star.core.agents.chain import create_git_commit_message_chain
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.message import Message
from gpt_all_star.helper.git import Git


class Deployment:
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        self.copilot = copilot

    def run(self) -> None:
        git = Git(self.copilot.storages.root.path)
        files_to_add = git.files()
        if not files_to_add:
            self.copilot.state("No files to add to the repository.")
            return

        self.copilot.state("The following diff will be pushed to the repository")
        syntax = Syntax(git.diffs(), "diff", theme="monokai", line_numbers=True)
        self.copilot.console.print(syntax)

        commit_info = create_git_commit_message_chain().invoke(
            {
                "messages": [
                    Message.create_human_message(
                        f"""
# Instructions
---
Generate an appropriate branch name and commit message showing the following diffs.

# Constraints
---
The format should follow Conventional Commits.

## Here is the diff
```
{git.diffs()}
```
"""
                    )
                ],
            }
        """
        Confirms the push to the repository.
        """
        """
        Confirms the push to the repository.
        """
        )

        self.copilot.console.new_lines()
        self.copilot.state("Pushing to the repository...")
        try:
            branch_name = (
                commit_info["branch"]
                if git.check_local_main_branch_exists()
                else "main"
            )
            is_main_branch = branch_name == "main"

            if not is_main_branch:
                git.checkout(branch_name)

            git.add(files_to_add)
            git.commit(commit_info["message"])
            git.push()

            if not is_main_branch:
                git.create_pull_request(branch_name)
        except Exception as e:
            self.copilot.state(
                f"An error occurred while pushing to the repository: {str(e)}"
            )
