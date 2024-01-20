import random
import string
import subprocess
from termcolor import colored
from rich.syntax import Syntax

from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.steps import step_prompts
from gpt_all_star.tool.git import Git
from gpt_all_star.logger.logger import logger


class Copilot(Agent):
    def __init__(
        self,
        storages: Storages | None = None,
        name: str = "copilot",
        profile: str = AgentRole.default_profile()[AgentRole.COPILOT].format(),
    ) -> None:
        super().__init__(AgentRole.COPILOT, storages, name, profile)

    def start(self, project_name: str) -> None:
        self.state(f"Let's start the project! ({project_name})")
        self._console.new_lines(1)

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

        logger.info(f"Completed project: {self.name}")

    def execute_code(self) -> None:
        command = self.storages.root["run.sh"]

        self._console.new_lines()
        print(
            colored(
                "Do you want to execute this code? (y/n)",
                "red",
            )
        )
        self._console.new_lines()
        print(command)
        self._console.new_lines()
        if input().lower() not in ["", "y", "yes"]:
            print("Ok, not executing the code.")
            return []
        print("Executing the code...")
        self._console.new_lines()
        print(
            colored(
                "Note: If it does not work as expected, please consider running the code"
                + " in another way than above.",
                "green",
            )
        )
        self._console.new_lines()
        print("You can press ctrl+c *once* to stop the execution.")
        self._console.new_lines()

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
            count = 0

            self._console.print(
                f"The following error occurred:\n{e.stderr}.\n Attempt to correct the source codes.\n",
                style="bold red",
            )
            for file_name, file_str in self._get_code_strings().items():
                self._console.print(
                    f"Adding file {file_name} to the prompt...", style="blue"
                )
                code_input = step_prompts.format_file_to_input(file_name, file_str)
                self.messages.append(Message.create_system_message(f"{code_input}"))

            self.messages.append(Message.create_system_message(e.stderr))

            self.chat(step_prompts.fix_source_code_template.format())
            response = self.latest_message_content()
            logger.info(f"response: {response}")
            self._console.new_lines(1)
            count += 1

            files = Message.parse_message(self.latest_message_content())
            for file_name, file_content in files:
                self.storages.root[file_name] = file_content

            self.execute_code()

        except KeyboardInterrupt:
            self._console.new_lines(1)
            self._console.print("Stopping execution.", style="bold yellow")
            self._console.print("Execution stopped.", style="bold red")
            self._console.new_lines(1)

    def _get_code_strings(self) -> dict[str, str]:
        return self.storages.root.recursive_file_search()

    def push_to_git_repository(self) -> None:
        git = Git(self.storages.root.path)
        files_to_add = git.files()
        if not files_to_add:
            logger.info("No files to add to the repository.")
            return

        self.state("The following diff will be pushed to the repository")
        syntax = Syntax(git.diffs(), "diff", theme="monokai", line_numbers=True)
        self._console.print(syntax)

        if not self._confirm_push():
            return

        self.messages.append(
            Message.create_system_message(
                step_prompts.generate_commit_message_template.format(diff=git.diffs())
            )
        )
        self.chat()
        commit_message = self.latest_message_content()

        self._console.new_lines(1)
        self.state("Pushing to the repository...")
        git.add(files_to_add)
        git.commit(commit_message)
        git.push()

    def _confirm_push(self):
        response = self.ask(
            "Continue with commit and push? (y/n)",
            is_required=False,
            default="y",
        )
        return response.lower() in ["", "y", "yes"]
