def create_additional_tasks() -> list:
    additional_tasks = [
        {
            "action": "Add a new file",
            "working_directory": ".",
            "filename": "ui_design.html",
            "command": "",
            "context": """The task is to clarify the user interface design and provide a user interface design in the html format.

First, list screen parts necessary to fully meet specifications.
Then, design user-friendly and aesthetically pleasing screen layouts in accordance with Material Design guidelines and principles.

It must be contained DOM structure and CSS needed to represent the screen design in one file.
""",
        },
    ]
    return additional_tasks
