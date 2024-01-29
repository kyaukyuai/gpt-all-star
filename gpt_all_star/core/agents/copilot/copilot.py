import random
import string
import subprocess
from termcolor import colored
from rich.syntax import Syntax

from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.copilot.create_commit_message_prompt import (
    create_commit_message_template,
)
from gpt_all_star.core.agents.copilot.fix_source_code_prompt import (
    fix_source_code_template,
)
from gpt_all_star.core.steps import step_prompts
from gpt_all_star.tool.git import Git
from gpt_all_star.tool.text_parser import TextParser


class Copilot(Agent):
    def __init__(
        self,
        storages: Storages | None = None,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.COPILOT, storages, name, profile)

    def start(self, project_name: str) -> None:
        self.state(f"Let's start the project! ({project_name})")
        self.console.new_lines(1)

    def ask_project_name(self) -> str:
        default_project_name = "".join(
            random.choice(string.ascii_letters + string.digits) for i in range(15)
        )
        project_name = self.ask(
            "What is the name of the project?",
            is_required=False,
            default=default_project_name,
        )
        return project_name

    def finish(self) -> None:
        self.ask(
            "Project is finished! Do you want to add any features or changes?"
            " If yes, describe it here and if no, just press ENTER",
            is_required=False,
            default=None,
        )
        self.state(f"Completed project: {self.name}")

    def execute_code(self, auto_mode: bool = False) -> None:
        command = self.storages.root["run.sh"]
        self._confirm_execution(auto_mode, command)
        self._run_command()

    def _confirm_execution(self, auto_mode: bool, command: str) -> None:
        if not auto_mode:
            self.console.new_lines()
            print(
                colored(
                    "Do you want to execute this code? (y/n)",
                    "red",
                )
            )
            self.console.new_lines()
            print(command)
            self.console.new_lines()
            if input().lower() not in ["", "y", "yes"]:
                print("Ok, not executing the code.")
                return []

        print("Executing the code...")
        self.console.new_lines()
        print(
            colored(
                "Note: If it does not work as expected, please consider running the code"
                + " in another way than above.",
                "green",
            )
        )
        self.console.new_lines()
        print("You can press ctrl+c *once* to stop the execution.")
        self.console.new_lines()

    def _run_command(self) -> None:
        command = "bash run.sh"
        try:
            subprocess.run(
                command,
                shell=True,
                cwd=self.storages.root.path,
                check=True,
                text=True,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            self._handle_error(e)
        except KeyboardInterrupt:
            self._handle_keyboard_interrupt()

    def _handle_error(self, e: subprocess.CalledProcessError) -> None:
        count = 0

        self.console.print(
            f"The following error occurred:\n{e.stderr}.\n Attempt to correct the source codes.\n",
            style="bold red",
        )
        for (
            file_name,
            file_str,
        ) in self.storages.root.recursive_file_search().items():
            self.console.print(
                f"Adding file {file_name} to the prompt...", style="blue"
            )
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            self.messages.append(Message.create_system_message(f"{code_input}"))

        self.messages.append(Message.create_system_message(e.stderr))

        self.chat(fix_source_code_template.format())
        self.console.new_lines(1)
        count += 1

        files = TextParser.parse_code_from_text(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.root[file_name] = file_content

        self.execute_code()

    def _handle_keyboard_interrupt(self) -> None:
        self.console.new_lines()
        self.console.print("Stopping execution.", style="bold yellow")
        self.console.print("Execution stopped.", style="bold red")
        self.console.new_lines()

    def push_to_git_repository(self, auto_mode: bool = False) -> None:
        git = Git(self.storages.root.path)
        files_to_add = git.files()
        if not files_to_add:
            self.state("No files to add to the repository.")
            return

        self.state("The following diff will be pushed to the repository")
        syntax = Syntax(git.diffs(), "diff", theme="monokai", line_numbers=True)
        self.console.print(syntax)

        if not (self._confirm_push() or auto_mode):
            return

        self.messages.append(
            Message.create_system_message(
                create_commit_message_template.format(
                    diff=git.diffs(),
                    json_format="""
{
    "commitDetails": {
        "type": "object",
        "description": "Details of the commit to be made.",
        "properties": {
            "branch": {
                "type": "string",
                "description": "Name of the branch to be pushed.",
            },
            "message": {
                "type": "string",
                "description": "Commit message to be used.",
            }
        },
        "required": ["branch", "message"],
    }
}
""",
                    example="""
------------------------example_1---------------------------
```
{
    "branch": "feat/feature-1",
    "message": "add feature 1",
}
```
------------------------example_1---------------------------
""",
                )
            )
        )
        self.chat()
        commit_details = TextParser.to_json(self.latest_message_content())[
            "commitDetails"
        ]

        self.console.new_lines()
        self.state("Pushing to the repository...")
        try:
            git.checkout(commit_details["branch"])
            git.add(files_to_add)
            git.commit(commit_details["message"])
            git.push()
            self.state("Push successful!")
        except Exception as e:
            self.state(f"An error occurred while pushing to the repository: {str(e)}")

    def _confirm_push(self):
        CONFIRM_CHOICES = ["yes", "no"]
        choice = self.present_choices(
            "Proceed with commit and push to repository?",
            CONFIRM_CHOICES,
            default=1,
        )
        return choice == "yes"
