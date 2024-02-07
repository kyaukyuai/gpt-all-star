from __future__ import annotations

import re

from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.agents.engineer.implement_improvement_prompt import (
    implement_improvement_template,
)
from gpt_all_star.core.agents.engineer.create_entrypoint_prompt import (
    create_entrypoint_template,
)
from gpt_all_star.core.agents.engineer.create_readme_prompt import (
    create_readme_template,
)
from gpt_all_star.core.agents.engineer.planning_improvement_prompt import (
    planning_improvement_template,
)
from gpt_all_star.helper.text_parser import TextParser


class Engineer(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.ENGINEER, storages, debug_mode, name, profile)

    def create_entrypoint(self, review_mode: bool = False):
        self.messages.append(
            Message.create_system_message(create_entrypoint_template.format())
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            review_mode=review_mode,
        )

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.root["run.sh"] = "\n".join(match.group(1) for match in matches)

    def create_readme(self, review_mode: bool = False):
        self.messages.append(
            Message.create_system_message(create_readme_template.format())
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            review_mode=review_mode,
        )

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.root["README.md"] = "\n".join(match.group(1) for match in matches)

    def improve_source_code(self, review_mode: bool = False):
        request = self.ask(
            "What would you like to update?", is_required=True, default=None
        )

        self.messages.append(
            Message.create_system_message(
                planning_improvement_template.format(
                    request=request,
                    specifications=self.storages.docs["specifications.md"],
                    codes=self.current_source_code(),
                    json_format="""
{
    "plan": {
        "type": "array",
        "description": "List of tasks to fully respond to user requests.",
        "items": {
            "type": "object",
            "description": "Task to fully respond to user requests.",
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
            "required": ["todo", "goal"],
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
        self.invoke()
        self.console.new_lines(2)

        todo_list = TextParser.to_json(self.latest_message_content())

        for i, task in enumerate(todo_list["plan"]):
            self.console.print(f"TODO {i + 1}: {task['todo']}")
            self.console.print(f"GOAL: {task['goal']}")
            self.console.new_lines()

            previous_finished_task_message = (
                "All preceding tasks have been completed. No further action is required on them.\n"
                + "All codes implemented so far are listed below. Please include them to ensure that we achieve our goal.\n"
                + f"{self.current_source_code()}\n\n"
                if i == 0
                else ""
            )
            self.messages.append(
                Message.create_system_message(
                    implement_improvement_template.format(
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
            self.invoke()
            self.console.new_lines(2)
            files = TextParser.parse_code_from_text(self.latest_message_content())
            for file_name, file_content in files:
                self.storages.root[file_name] = file_content

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            review_mode=review_mode,
        )
