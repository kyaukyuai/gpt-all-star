import json
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.execution import Execution
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team
from gpt_all_star.core.implement_planning_prompt import (
    implement_planning_template,
)


class Improvement(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        team = Team(
            supervisor=self.agents.project_manager,
            members=[
                self.agents.engineer,
                self.agents.designer,
                self.agents.qa_engineer,
            ],
        )

        request = self.agents.engineer.ask(
            "What would you like to update?", is_required=True, default=None
        )

        todo_list = self.agents.project_manager.create_planning_chain().invoke(
            {
                "messages": [
                    Message.create_human_message(
                        f"""
# Instructions
---
Create a detailed and specific development plan to fully meet the user's requirements.

# Constraints
---
Must always fulfill the user's request exactly.
## request

```plaintext
{request}
```

# Current implementation
---
```
{self.agents.project_manager.current_source_code()}
```
"""
                    )
                ],
            },
        )

        print(json.dumps(todo_list, indent=4))

        for i, task in enumerate(todo_list["plan"]):
            team.supervisor.state(
                f"""\n
Task {i + 1}: {task['task']}
Objective: {task['objective']}
Reason: {task['reason']}
---
"""
            )

            if task["task"] == "executing a command":
                todo = f"{task['task']}: {task['command']} in the directory {task['working_directory']}"
            else:
                todo = f"{task['task']}: {task['working_directory']}/{task['filename']}"
            message = Message.create_human_message(
                implement_planning_template.format(
                    task=todo,
                    objective=task["objective"],
                    context=task["context"],
                    reason=task["reason"],
                    implementation=self.agents.project_manager.current_source_code(),
                    specifications=self.agents.project_manager.storages.docs[
                        "specifications.md"
                    ],
                )
            )
            team.run([message])

        CONFIRM_CHOICES = ["yes", "no"]
        choice = self.agents.copilot.present_choices(
            "Do you want to check the execution again?",
            CONFIRM_CHOICES,
            default=1,
        )
        if choice == CONFIRM_CHOICES[0]:
            Execution(
                self.agents, self.japanese_mode, self.review_mode, self.debug_mode
            ).run()
