import json

from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.implement_planning_prompt import implement_planning_template
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


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
Create a detailed and specific development plan from project creation to source code implementation, testing, and operation verification in order to build a correctly working application.

# Constraints
---
The application specifications must be carefully understood and accurately reflect the specifications.

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
                "filename": "N/A",
                "command": "N/A",
                "context": """This task involves actively implementing any files identified as missing or incomplete from the docs/files.md review, in accordance with the project specifications.
The focus is on directly addressing and filling in the gaps in the codebase to ensure completeness and functionality.
""",
                "objective": """To directly implement the missing functionalities or complete the partial implementations identified during the review of docs/files.md.
This action will ensure that the project is fully developed and conforms to the intended design and functionality specifications.
""",
                "reason": """Ensuring that all components of the project are implemented according to specifications is essential for the project's integrity and success.
Directly addressing any missing or incomplete files is crucial for eliminating discrepancies and enhancing the project's overall quality and reliability.
This approach guarantees that the application functions as intended and fulfills user requirements effectively.
""",
            },
            {
                "task": "Add a new file",
                "working_directory": "./",
                "filename": "run.sh",
                "command": "N/A",
                "context": """The run.sh script is created to automate the setup and execution processes within the project without needing global installations or superuser privileges.
It encapsulates commands for locally installing dependencies, setting environment variables,
and starting necessary parts of the codebase in parallel, adhering to security best practices and project-specific requirements.
""",
                "objective": """To facilitate a seamless setup and launch of the application by automating these processes through a script.
This eliminates the need for manual execution of each step, thereby reducing potential human errors and ensuring consistency across different environments.
""",
                "reason": """Creating a run.sh file is crucial for maintaining an efficient and secure development workflow.
It allows any developer to easily prepare and run the application's environment with a single command, without the risk associated with global installations or the need for administrative rights.
This approach not only safeguards the system's integrity but also enhances the portability and accessibility of the project across various development environments.
""",
            },
            {
                "task": "Add a new file",
                "working_directory": "./",
                "filename": "README.md",
                "command": "N/A",
                "context": """The README.md file is the gateway to understanding the project,
providing essential details such as the project title, a brief description, the technology stack used, requirements for running the project, and instructions on how to run it.
This comprehensive overview ensures that anyone looking at the project for the first time can quickly grasp its purpose, setup, and usage.
""",
                "objective": """To craft a document that serves as a complete guide for navigating and understanding the project.
The README aims to succinctly communicate the project's title, its core functionalities and features, the technologies it is built upon,
any prerequisites or dependencies needed for installation, and clear, step-by-step instructions for running the project.
""",
                "reason": """Including a well-documented README file is crucial for any project, especially open-source ones,
as it significantly boosts the project's clarity and ease of use for both potential users and contributors.
It acts as the first layer of documentation that aids in setting the right expectations and providing a roadmap for engagement with the project.
This not only enhances the project's approachability but also fosters a welcoming environment for collaboration and contribution.
""",
            },
        ]
        for task in additional_tasks:
            todo_list["plan"].append(task)

        nodejs_tasks = [
            {
                "task": "Read and Overwrite an existing file",
                "working_directory": "./",
                "filename": "the specific file with placeholders",
                "command": "N/A",
                "context": """The task involves identifying a file within the project that has incomplete implementation,
indicated by placeholders such as 'will go here', 'will be added here', 'PlaceHolder', 'TODO', etc.
Once identified, these placeholders are to be addressed and corrected with complete and functional code to ensure that the implementation is fully realized.
""",
                "objective": """To remove any uncertainties or incomplete segments within the code by replacing placeholders with actual, working code.
This aims to enhance the code's integrity and functionality, ensuring that the implementation is comprehensive and devoid of omissions.
""",
                "reason": """Completing the implementation by addressing placeholders is crucial for maintaining a high standard of code quality.
It ensures that the project is reliable, maintainable, and free from sections that could lead to confusion or errors during execution.
This task directly impacts the project's effectiveness and its ability to meet its intended functionalities.
""",
            },
            {
                "task": "Read and Overwrite an existing file",
                "working_directory": "./",
                "filename": "package.json",
                "command": "N/A",
                "context": """The task requires setting the NODE_OPTIONS environment variable to '--openssl-legacy-provider' within the package.json file for a NodeJS project.
This is done by adding specific lines to the 'start' and 'build' scripts, enabling the application to use the OpenSSL legacy provider mode.
""",
                "objective": """To configure the NodeJS environment to use the OpenSSL legacy provider, which may be necessary for compatibility with certain encryption standards or libraries.
This configuration ensures that the project can be built and started without issues related to OpenSSL.
""",
                "reason": """Setting the NODE_OPTIONS environment variable is essential for ensuring that the project's dependencies that rely on OpenSSL can operate correctly under the current NodeJS version.
This change mitigates potential issues related to the newer OpenSSL library versions by explicitly instructing NodeJS to use the legacy provider, thereby ensuring the project's smooth operation and development.
""",
            },
            {
                "task": "Read and Overwrite an existing file",
                "working_directory": "./",
                "filename": "package.json",
                "command": "N/A",
                "context": """The task involves modifying the package.json file of a NodeJS project by removing the 'homepage' item.
This item may have been previously set for deployment or documentation purposes, but is now required to be omitted.
""",
                "objective": """To update the package.json file to reflect the current project requirements accurately, which includes the removal of the homepage item.
This ensures that the package.json file only contains necessary and relevant information.""",
                "reason": """Removing the 'homepage' item from package.json is a strategic step to prevent potential conflicts or misconfigurations during deployment or package management.
It streamlines the project's configuration, making it more straightforward and aligned with its current goals and deployment strategies.
""",
            },
            {
                "task": "Read and Overwrite an existing file",
                "working_directory": "./",
                "filename": "package.json",
                "command": "N/A",
                "context": """This task involves a thorough review of the package.json file within a NodeJS project to ensure that all library dependencies listed are currently in use,
adequately up-to-date, and that no necessary libraries are missing.
This process includes validating each dependency to match the project's requirements, removing unused or deprecated libraries, and adding any missing libraries essential for the project's functionality.
""",
                "objective": """To optimize the project's dependency tree by ensuring that only relevant and necessary libraries are included in the package.json file.
This aims to enhance project efficiency by minimizing bloat, reducing installation times, and ensuring compatibility across all dependencies.
""",
                "reason": """Maintaining an accurate and lean list of dependencies is crucial for the health and maintainability of the project.
It prevents potential conflicts, reduces security vulnerabilities from outdated or unnecessary packages, and ensures that the project's setup remains streamlined and efficient.
This task directly contributes to the stability, security, and performance of the project.
""",
            },
        ]
        for task in nodejs_tasks:
            todo_list["plan"].append(task)

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
