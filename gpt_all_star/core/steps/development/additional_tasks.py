additional_tasks = [
    {
        "action": "Add a new file",
        "working_directory": "./app/",
        "filename": "",
        "command": "",
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
        "action": "Add a new file",
        "working_directory": "./app",
        "filename": "run.sh",
        "command": "",
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
        "action": "Add a new file",
        "working_directory": "./app",
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
]
