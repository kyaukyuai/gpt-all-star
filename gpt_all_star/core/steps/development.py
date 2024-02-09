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
Create a development plan according to the following requirements.

# Constraints
---
The TODO must be one of executing a command, adding a new file, modifying an existing file, or deleting an existing file.

# Requirements
---

## Application Specifications
```
{self.agents.project_manager.storages.docs["specifications.md"]}
```

## Technology stack
```
{self.agents.project_manager.storages.docs["technologies.md"]}
```

## Page URL
```
{self.agents.project_manager.storages.docs["pages.md"]}
```

## Files
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
TODO {i + 1}: {task['todo']}
DETAIL: {task['detail']}
DIRECTORY: {task['working_directory']}
GOAL: {task['goal']}
---
"""
            )

            message = Message.create_human_message(
                implement_planning_template.format(
                    todo=task["todo"],
                    detail=task["detail"],
                    directory=task["working_directory"],
                    goal=task["goal"],
                    specifications=self.agents.project_manager.storages.docs[
                        "specifications.md"
                    ],
                )
            )
            team.run([message])

        self.agents.engineer.create_entrypoint(review_mode=self.review_mode)
        self.agents.engineer.create_readme(review_mode=self.review_mode)
        self.agents.qa_engineer.check_code(review_mode=self.review_mode)
