def create_additional_tasks() -> list:
    additional_tasks = [
        {
            "action": "Add a new file",
            "working_directory": ".",
            "filename": "technologies.md",
            "command": "",
            "context": """The task is to clarify the technology requirements to be used for the project and provide a list of technology requirements in the markdown format.

First, list only the most used and minimum required technologies in the project in order to build an application that meets the specifications.
Then, select only the technologies that related to source code implementation, not version control tools, technologies related to automated testing or deployment, or tools related to project management.

It must be included in the document.
---
1. Development language

2. Framework

3. Library
""",
        },
    ]
    return additional_tasks
