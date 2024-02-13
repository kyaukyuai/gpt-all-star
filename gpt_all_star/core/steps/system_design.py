from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.implement_planning_prompt import implement_planning_template
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class SystemDesign(Step):
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
                self.agents.architect,
                self.agents.designer,
                self.agents.engineer,
            ],
        )
        todo_list = {
            "plan": [
                {
                    "task": "Add a new file",
                    "working_directory": "./docs/",
                    "filename": "technologies.md",
                    "command": "",
                    "context": """This task requires compiling a precise list of technologies for building an application,
focusing on source code implementation. The list should adhere to project specifications and be guided by Technologies Guidelines emphasizing relevance, compatibility, and preference.
These guidelines mandate including only essential, actively used technologies, ensuring their compatibility,
and excluding any that cannot be integrated. Additionally, when multiple options are available for a specific project component, the guidelines prioritize React, JavaScript, chakra-ui, HTML, and Docker / Docker Compose.
""",
                    "objective": """To produce a document clearly outlining the necessary and compatible technologies for the project's development, prioritizing preferred technologies.
This aims to ensure an efficient and coherent development process using a streamlined, compatible technology stack, thereby facilitating easier integration and implementation.
""",
                    "reason": """Creating a focused and guided list of technologies is essential for the project's success.
It enables the development team to make informed decisions about the technology stack, ensuring that each technology chosen is not only relevant and compatible but also preferred within the project's context.
This approach minimizes integration issues, optimizes development efforts, and ensures the project is built on a solid and efficient foundation of technologies well-suited to its requirements.
""",
                },
                {
                    "task": "Add a new file",
                    "working_directory": "./docs/",
                    "filename": "pages.md",
                    "command": "",
                    "context": """This task involves identifying and listing the exact page URLs required for the application's operation.
The focus is on compiling a comprehensive list of URLs that are essential for navigating and utilizing the application, without the need for additional descriptions or explanations for each URL.
The task emphasizes the importance of precision and relevance in selecting only those URLs that are necessary for the application, excluding any personal opinions or alternative suggestions.
""",
                    "objective": """To create a succinct document that enumerates all critical page URLs for the application, providing a clear and straightforward reference for developers and users alike.
This document aims to facilitate understanding of the application's structure and navigation by listing the URLs required for accessing its various components and features.
""",
                    "reason": """Compiling a list of necessary page URLs is crucial for the efficient development and use of the application.
It ensures that all stakeholders have a clear understanding of the application's layout and how to interact with it.
This approach aids in streamlining the navigation design, eliminating any unnecessary or redundant pages, and focusing on the application's core functionalities.
By providing a direct and unambiguous list of page URLs, the project supports a more organized and user-friendly interface.
""",
                },
                {
                    "task": "Add a new file",
                    "working_directory": "./docs/",
                    "filename": "files.md",
                    "command": "",
                    "context": """Your task is to make sure you have an exhaustive list of all file names needed for the application.
Follow a language and framework appropriate best practice file naming convention.
Descriptions for each file name are not required, only provide the exact file path and file name.
Avoid providing personal opinions or alternatives.
""",
                    "objective": """To compile a comprehensive list of all necessary file names and paths required for the application,
adhering to best practices in file naming conventions appropriate to the programming language and framework used.
This list will serve as a definitive guide for developers to understand the structure and components of the application.
""",
                    "reason": """Ensuring a complete and well-organized list of file names is crucial for the clarity and maintainability of the application.
Following best practice conventions aids in the systematic organization of files, making it easier for developers to navigate, understand, and collaborate on the project.
This practice promotes consistency, reduces confusion, and enhances the overall development workflow.
""",
                },
            ]
        }
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
                    implementation=None,
                    specifications=self.agents.project_manager.storages.docs[
                        "specifications.md"
                    ],
                )
            )
            team.run([message])
