from rich.syntax import Syntax

from gpt_all_star.cli.console_terminal import ConsoleTerminal
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.helper.git import Git


class Deployment:
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        self.console = ConsoleTerminal()
        self.agents = agents
        self.japanese_mode = japanese_mode
        self.review_mode = review_mode
        self.debug_mode = debug_mode

    def run(self) -> None:
        git = Git(self.agents.copilot.storages.root.path)
        files_to_add = git.files()
        if not files_to_add:
            self.agents.copilot.state("No files to add to the repository.")
            return

        self.agents.copilot.state("The following diff will be pushed to the repository")
        syntax = Syntax(git.diffs(), "diff", theme="monokai", line_numbers=True)
        self.console.print(syntax)

        if not self.agents.copilot.confirm_push() and self.review_mode:
            return

        commit_info = self.agents.copilot.create_git_commit_message_chain().invoke(
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

        self.agents.copilot.console.new_lines()
        self.agents.copilot.state("Pushing to the repository...")
        try:
            git.checkout(commit_info["branch"])
            git.add(files_to_add)
            git.commit(commit_info["message"])
            git.push()
            self.agents.copilot.state("Push successful!")
        except Exception as e:
            self.agents.copilot.state(
                f"An error occurred while pushing to the repository: {str(e)}"
            )
