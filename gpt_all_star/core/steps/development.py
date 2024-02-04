from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.team import Team
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.agents.engineer.implement_planning_prompt import (
    implement_planning_template,
)


class Development(Step):
    def __init__(
        self, agents: Agents, japanese_mode: bool, auto_mode: bool, debug_mode: bool
    ) -> None:
        super().__init__(agents, japanese_mode, auto_mode, debug_mode)

    def run(self) -> None:
        team = Team(
            supervisor=self.agents.copilot,
            members=[
                self.agents.engineer,
                self.agents.designer,
                self.agents.qa_engineer,
            ],
        )

        todo_list = self.agents.engineer.plan_development(auto_mode=self.auto_mode)
        for i, task in enumerate(todo_list["plan"]):
            self.console.print(f"TODO {i + 1}: {task['todo']}")
            self.console.print(f"GOAL: {task['goal']}")
            self.console.print("---")

            previous_finished_task_message = f"""The information given to you is as follows.
There are the specifications to build the application:
```
{self.agents.copilot.storages.docs["specifications.md"]}
```

There are the source codes generated so far:
```
{self.agents.copilot.current_source_code()}
```
"""
            message = Message.create_human_message(
                implement_planning_template.format(
                    todo_description=task["todo"],
                    finished_todo_message=previous_finished_task_message,
                    todo_goal=task["goal"],
                )
            )
            team.run([message])

        self.agents.engineer.create_source_code(auto_mode=self.auto_mode)
        self.agents.engineer.complete_source_code(auto_mode=self.auto_mode)
        self.console.new_lines()
