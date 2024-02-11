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
Create a detailed and specific development plan to meet the application requirements and build a complete application.

# Constraints
---
- The `task` must be one of "Execute a command", "Add a new file", "Read and Overwrite an existing file", or "Delete an existing file".

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

        additional_tasks = [
            {
                "task": "Add a new file",
                "working_directory": "./",
                "filename": "run.sh",
                "context": "The run.sh script is created to automate the setup and execution processes within the project without needing global installations or superuser privileges. It encapsulates commands for locally installing dependencies, setting environment variables, and starting necessary parts of the codebase in parallel, adhering to security best practices and project-specific requirements.",
                "objective": "To facilitate a seamless setup and launch of the application by automating these processes through a script. This eliminates the need for manual execution of each step, thereby reducing potential human errors and ensuring consistency across different environments.",
                "reason": "Creating a run.sh file is crucial for maintaining an efficient and secure development workflow. It allows any developer to easily prepare and run the application's environment with a single command, without the risk associated with global installations or the need for administrative rights. This approach not only safeguards the system's integrity but also enhances the portability and accessibility of the project across various development environments.",
            },
            {
                "task": "Add a new file",
                "working_directory": "./",
                "filename": "README.md",
                "context": "The README.md file is the gateway to understanding the project, providing essential details such as the project title, a brief description, the technology stack used, requirements for running the project, and instructions on how to run it. This comprehensive overview ensures that anyone looking at the project for the first time can quickly grasp its purpose, setup, and usage.",
                "objective": "To craft a document that serves as a complete guide for navigating and understanding the project. The README aims to succinctly communicate the project's title, its core functionalities and features, the technologies it is built upon, any prerequisites or dependencies needed for installation, and clear, step-by-step instructions for running the project.",
                "reason": "Including a well-documented README file is crucial for any project, especially open-source ones, as it significantly boosts the project's clarity and ease of use for both potential users and contributors. It acts as the first layer of documentation that aids in setting the right expectations and providing a roadmap for engagement with the project. This not only enhances the project's approachability but also fosters a welcoming environment for collaboration and contribution.",
            },
        ]
        for task in additional_tasks:
            todo_list["plan"].append(task)

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
                    reason=task["reason"],
                    implementation=self.agents.project_manager.current_source_code(),
                    specifications=self.agents.project_manager.storages.docs[
                        "specifications.md"
                    ],
                )
            )
            team.run([message])

        self.agents.qa_engineer.check_code(review_mode=self.review_mode)
