import json

from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.implement_planning_prompt import implement_planning_template
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class UIDesign(Step):
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
        todo_list = self.agents.project_manager.create_planning_chain().invoke(
            {
                "messages": [
                    Message.create_human_message(
                        f"""
# Instructions
---
Create a detailed and specific development plan to enhance the UI and UX in accordance with human interface guideline.

# Constraints
---
The application specifications must be carefully understood and accurately reflect the specifications.

# Current implementation
---
```
{self.agents.project_manager.current_source_code()}
```

# Specifications
---
```
{self.agents.project_manager.storages.docs["specifications.md"]}
```
"""
                    )
                ],
            },
        )

        print(json.dumps(todo_list, indent=4))

        for i, task in enumerate(todo_list["plan"]):
            if task["task"] == "Execute a command":
                todo = f"{task['task']}: {task['command']} in the directory {task['working_directory']}"
            else:
                todo = f"{task['task']}: {task['working_directory']}/{task['filename']}"

            team.supervisor.state(
                f"""\n
Task {i + 1}: {todo}
Context: {task['context']}
Objective: {task['objective']}
Reason: {task['reason']}
---
"""
            )

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
