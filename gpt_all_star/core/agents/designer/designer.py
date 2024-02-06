from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.designer.planning_ui_design_prompt import (
    planning_ui_design_template,
)
from gpt_all_star.core.agents.designer.implement_planning_prompt import (
    implement_planning_template,
)
from gpt_all_star.helper.text_parser import TextParser


class Designer(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.DESIGNER, storages, debug_mode, name, profile)

    def design_user_interface(self, review_mode: bool = False):
        self.messages.append(
            Message.create_system_message(
                planning_ui_design_template.format(
                    specifications=self.storages.docs["specifications.md"],
                    codes=self.current_source_code(),
                    json_format="""
{
    "plan": {
        "type": "array",
        "description": "List of tasks to enhance the UI and UX to be as stylish and trendy as an iPhone.",
        "items": {
            "type": "object",
            "description": "Task to enhance the UI and UX to be as stylish and trendy as an iPhone.",
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
                    implement_planning_template.format(
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
