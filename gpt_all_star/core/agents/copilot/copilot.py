import random
import string
import subprocess
from rich.syntax import Syntax

from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.copilot.planning_healing_prompt import (
    planning_healing_template,
)
from gpt_all_star.core.agents.copilot.implement_planning_prompt import (
    implement_planning_prompt_template,
)
from gpt_all_star.core.agents.copilot.create_commit_message_prompt import (
    create_commit_message_template,
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
            CONFIRM_CHOICES = ["yes", "no"]
            choice = self.present_choices(
                "Do you want to execute this code?",
                CONFIRM_CHOICES,
                default=1,
            )
            self.console.new_lines()
            self.console.print(command)
            self.console.new_lines()
            if choice == CONFIRM_CHOICES[1]:
                print("Ok, not executing the code.")
                return []

        self.state("Executing the code...")
        self.console.new_lines()
        self.state(
            "If it does not work as expected, please consider running the code"
            + " in another way than above."
        )
        self.console.new_lines()
        self.state("You can press ctrl+c *once* to stop the execution.")
        self.console.new_lines()

    def _run_command(self) -> None:
        command = "bash run.sh"
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.state(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}")
            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    cwd=self.storages.root.path,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                self.console.print(result.stdout, style="green")
                self.console.print(result.stderr, style="red")
                if result.returncode == 0:
                    break
                else:
                    self._handle_error(
                        {"stdout": result.stdout, "stderr": result.stderr}
                    )
            except KeyboardInterrupt:
                self._handle_keyboard_interrupt()
                break

    def _handle_error(self, e: dict) -> None:
        self.state("Initiating source code correction process.")

        current_codes = ""
        for (
            file_name,
            file_str,
        ) in self.storages.root.recursive_file_search().items():
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            current_codes += f"{code_input}\n"

        self.messages.append(
            Message.create_system_message(
                planning_healing_template.format(
                    errors=e,
                    codes=current_codes,
                    json_format="""
{
    "plan": {
        "type": "array",
        "description": "List of tasks to fix the errors.",
        "items": {
            "type": "object",
            "description": "Task to fix the errors.",
            "properties": {
                "todo": {
                    "type": "string",
                    "description": "Very detailed description of the actual TODO to be performed to accomplish the entire plan.",
                },
                "goal": {
                    "type": "string",
                    "description": "Very detailed description of the goals to be achieved for the TODO to be executed to accomplish the entire plan",
                }
            },
            "required": ["todo", "goal", "review"],
        },
    }
}
""",
                    example="""
------------------------example_1---------------------------
```
{
    "plan": [
        {
            "todo": "",
            "goal": "",
        },
        {
            "todo": "",
            "goal": "",
        }
    ]
}
```
------------------------example_1---------------------------
""",
                )
            )
        )
        self.chat()
        self.console.new_lines(2)

        todo_list = TextParser.to_json(self.latest_message_content())
        self.console.print(todo_list)

        for i, task in enumerate(todo_list["plan"]):
            self.console.print(f"TODO {i + 1}: {task['todo']}")
            self.console.print(f"GOAL: {task['goal']}")
            self.console.new_lines()

            current_contents = ""
            for (
                file_name,
                file_str,
            ) in self.storages.root.recursive_file_search().items():
                self.console.print(
                    f"Adding file {file_name} to the prompt...", style="blue"
                )
                code_input = step_prompts.format_file_to_input(file_name, file_str)
                current_contents += f"{code_input}\n"

            previous_finished_task_message = (
                "All preceding tasks have been completed. No further action is required on them.\n"
                + "All codes implemented so far are listed below. Please include them to ensure that we achieve our goal.\n"
                + "{current_contents}\n\n"
                if i == 0
                else ""
            )
            self.messages.append(
                Message.create_system_message(
                    implement_planning_prompt_template.format(
                        num_of_todo=len(todo_list["plan"]),
                        todo_list="".join(
                            [
                                f"{i + 1}: {task['todo']}\n"
                                for i, task in enumerate(todo_list["plan"])
                            ]
                        ),
                        index_of_todo=i + 1,
                        todo_description=task["todo"],
                        finished_todo_message=previous_finished_task_message,
                        todo_goal=task["goal"],
                    )
                )
            )
            self.chat()
            self.console.new_lines(2)
            files = TextParser.parse_code_from_text(self.latest_message_content())
            for file_name, file_content in files:
                self.storages.root[file_name] = file_content

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
        return choice == CONFIRM_CHOICES[0]
