from __future__ import annotations

from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.agents.project_manager.planning_development_prompt import (
    planning_development_template,
)
from gpt_all_star.helper.text_parser import TextParser


class ProjectManager(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.PROJECT_MANAGER, storages, debug_mode, name, profile)

    def plan_development(self, review_mode: bool = False):
        self.messages.append(
            Message.create_system_message(
                planning_development_template.format(
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
            "goal": ""
        },
        {
            "todo": "",
            "goal": ""
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
            review_mode=review_mode,
        )

        return TextParser.to_json(self.latest_message_content())
