from __future__ import annotations
import json

import re

from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.agents.engineer.planning_development_prompt import (
    planning_development_prompt_template,
)
from gpt_all_star.core.agents.engineer.implement_planning_prompt import (
    implement_planning_prompt_template,
)
from gpt_all_star.core.agents.engineer.review_source_code_prompt import (
    review_source_code_template,
)
from gpt_all_star.core.agents.engineer.create_source_code_prompt import (
    create_source_code_template,
)
from gpt_all_star.core.agents.engineer.create_entrypoint_prompt import (
    create_entrypoint_template,
)
from gpt_all_star.core.agents.engineer.create_readme_prompt import (
    create_readme_template,
)
from gpt_all_star.core.agents.engineer.improve_source_code_prompt import (
    improve_source_code_template,
)
from gpt_all_star.core.steps import step_prompts
from gpt_all_star.tool.text_parser import TextParser


class Engineer(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.ENGINEER, storages, name, profile)

    def create_source_code(self, auto_mode: bool = False):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                planning_development_prompt_template.format(
                    specifications=self.storages.docs["specifications.md"],
                    technologies=self.storages.docs["technologies.md"],
                    pages=self.storages.docs["pages.md"],
                    files=self.storages.docs["files.md"],
                    json_format="""
{
    "plan": {
        "type": "array",
        "description": "List of development tasks that need to be done to implement the entire plan.",
        "items": {
            "type": "object",
            "description": "Development task that needs to be done to implement the entire plan. It contains all details that developer who is not familiar with project needs to know to implement the task.",
            "properties": {
                "todo": {
                    "type": "string",
                    "description": "Very detailed description of the actual TODO to be performed to accomplish the entire plan.",
                },
                "goal": {
                    "type": "string",
                    "description": "Very detailed description of the goals to be achieved for the TODO to be executed to accomplish the entire plan",
                },
                "review": {
                    "type": "string",
                    "description": "Very detailed description of what needs to be done to ensure that the goal has been achieved",
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
            "review": ""
        },
        {
            "todo": "",
            "goal": "",
            "review": ""
        }
    ]
}
```
------------------------example_1---------------------------
""",
                ),
            )
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

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

            self.console.print(f"REVIEW: {task['review']}")
            self.console.new_lines()

            self.messages.append(
                Message.create_system_message(
                    review_source_code_template.format(
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
                        todo_review=task["review"],
                    )
                )
            )
            self.chat()
            self.console.new_lines(2)
            files = TextParser.parse_code_from_text(self.latest_message_content())
            for file_name, file_content in files:
                self.storages.root[file_name] = file_content

        # self.messages.append(
        #     Message.create_system_message(
        #         create_source_code_template.format(
        #             specifications=self.storages.docs["specifications.md"],
        #             technologies=self.storages.docs["technologies.md"],
        #             pages=self.storages.docs["pages.md"],
        #             files=self.storages.docs["files.md"],
        #         ),
        #     )
        # )

        # self.execute(
        #     "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
        #         NEXT_COMMAND
        #     ),
        #     auto_mode=auto_mode,
        # )

        # files = TextParser.parse_code_from_text(self.latest_message_content())
        # for file_name, file_content in files:
        #     self.storages.root[file_name] = file_content

        self._create_entrypoint(auto_mode)
        self._create_readme(auto_mode)

    def _create_entrypoint(self, auto_mode: bool = False):
        self.messages.append(
            Message.create_system_message(create_entrypoint_template.format())
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.root["run.sh"] = "\n".join(match.group(1) for match in matches)

    def _create_readme(self, auto_mode: bool = False):
        self.messages.append(
            Message.create_system_message(create_readme_template.format())
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.root["README.md"] = "\n".join(match.group(1) for match in matches)

    def improve_source_code(self, auto_mode: bool = False):
        self.messages.append(
            Message.create_system_message(improve_source_code_template.format())
        )
        for file_name, file_str in self.storages.root.recursive_file_search().items():
            self.console.print(
                f"Adding file {file_name} to the prompt...", style="blue"
            )
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            self.messages.append(Message.create_system_message(f"{code_input}"))

        response = self.ask(
            "What would you like to update?", is_required=False, default=None
        )
        if response is not None:
            self.messages.append(Message.create_system_message(response))
        else:
            return

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        files = TextParser.parse_code_from_text(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.root[file_name] = file_content
