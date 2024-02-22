from rich.syntax import Syntax

from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.chain import create_git_commit_message_chain
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.helper.git import Git


class Deployment:
    def __init__(
        self,
        storages: Storages,
        copilot: Copilot,
        agents: Agents,
    ) -> None:
        self.storages = storages
        self.copilot = copilot
        self.agents = agents

    def run(self) -> None:
        git = Git(self.storages.root.path)
        files_to_add = git.files()
        if not files_to_add:
            self.copilot.state("No files to add to the repository.")
            return

        self.copilot.state("The following diff will be pushed to the repository")
        syntax = Syntax(git.diffs(), "diff", theme="monokai", line_numbers=True)
        self.copilot.console.console.print(syntax)

        if not self.copilot.confirm_push():
            return

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
        )

        self.copilot.console.new_lines()
        self.copilot.state("Pushing to the repository...")
        try:
            git.checkout(commit_info["branch"])
            git.add(files_to_add)
            git.commit(commit_info["message"])
            git.push()
            self.copilot.state("Push successful!")
        except Exception as e:
            self.copilot.state(
                f"An error occurred while pushing to the repository: {str(e)}"
            )
