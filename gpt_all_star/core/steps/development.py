import json
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.team import Team
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.agents.project_manager.implement_planning_prompt import (
    implement_planning_template,
)


class Development(Step):
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
Create your execution plan based on your current implementation and application requirements.

# Constraints
---
- The `task` must be one of executing a command, adding a new file, reading and overwriting an existing file, or deleting an existing file.

# Current implementation
---
```
{self.agents.project_manager.current_source_code()}
```

# Requirements
---

## Application Specifications to be met
```
{self.agents.project_manager.storages.docs["specifications.md"]}
```

## Technology stack to be used
```
{self.agents.project_manager.storages.docs["technologies.md"]}
```

## Page URL to be implemented
```
{self.agents.project_manager.storages.docs["pages.md"]}
```

## Files to be implemented
```
{self.agents.project_manager.storages.docs["files.md"]}
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
Justification: {task['justification']}
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
                    justification=task["justification"],
                    implementation=self.agents.project_manager.current_source_code(),
                    specifications=self.agents.project_manager.storages.docs[
                        "specifications.md"
                    ],
                )
            )
            team.run([message])

        self.agents.engineer.create_entrypoint(review_mode=self.review_mode)
        self.agents.engineer.create_readme(review_mode=self.review_mode)
        self.agents.qa_engineer.check_code(review_mode=self.review_mode)
