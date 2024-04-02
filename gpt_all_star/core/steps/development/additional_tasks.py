additional_tasks = [
    {
        "action": "Read and Overwrite an existing file",
        "working_directory": "",
        "filename": "the specific file with placeholders",
        "command": "",
        "context": """The task involves identifying a file within the project that has incomplete implementation,
indicated by placeholders such as 'will go here', 'will be added here', 'PlaceHolder', 'TODO', 'Component' etc.
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
        "action": "Read and Overwrite an existing file",
        "working_directory": "the directory where the target file exists",
        "filename": "README.md",
        "command": "",
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
    {
        "action": "Always need to make sure that source code and resources relevant to the project are stored in the correct location",
        "working_directory": "the directory where the target file exists",
        "filename": "README.md",
        "command": "",
        "context": """It is important that the correct implementation is made in the correct location according to the specifications of the technology used
If files or directories are not placed where they should be, the application will not run properly.
""",
        "objective": """Based on the specifications of the technology used, files and directories must be placed in the correct location during implementation.
If a file or directory is placed in the wrong location, it must be moved to the proper location.
""",
        "reason": """If the file or directories is in the wrong location, an error will occur and it will not work correctly.

Also, the file location is closely related to the import paths listed in the source code, and if the paths do not match, it is not a correct implementation.
""",
    },
]
