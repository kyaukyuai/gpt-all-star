additional_tasks = [
    {
        "action": "Add a new file",
        "working_directory": ".",
        "filename": "technologies.md",
        "command": "",
        "context": """[the task you do]
This task requires compiling a list of specific technologies to be used to build the application before starting the implementation of the source code.
This list must conform to the project specifications.
It must not use any technology unrelated to the project.
Must be compatible between the libraries used.
Additionally, when multiple options are available for a specific project component, the guidelines prioritize React, JavaScript, chakra-ui and HTML.
[output format]
Categorized by technology used and displayed in a list
For OSS, etc., if a Github repository exists, the URL must also be included.
If it does not exist, you do not need to include it.

[Important]
Only technologies related to source code implementation should be listed, not version control tools, technologies related to automated testing or deployment, or tools related to project management.
Descriptions for each technology are not required, only provide the exact technology name.
Avoid providing personal opinions or alternatives.
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
        "action": "Add a new file",
        "working_directory": ".",
        "filename": "system_architecture.md",
        "command": "",
        "context": """[the task you do]
In this task, you must create the screen transition diagrams needed to build the application before you can start implementing the source code
The screen transition diagrams should be text-based diagrams using mermaid.
[output format]
Generate a screen transition diagram according to the mermaid format.

""",
        "objective": """Reduce ambiguity in software development, allowing engineers to implement based on the design without hesitation.
""",
        "reason": """Development teams can learn more about deliverables
Understanding the details improves implementation accuracy and reduces rework, such as creating deliverables that differ from instructions.
""",
    },
]
