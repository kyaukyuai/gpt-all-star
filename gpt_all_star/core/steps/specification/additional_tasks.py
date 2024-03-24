def create_additional_tasks(app_type, instructions):
    additional_tasks = [
        {
            "action": "Add a new file",
            "working_directory": ".",
            "filename": "specifications.md",
            "command": "",
            "context": f"""Your task is to clarify the {app_type} specification.
Your role is to read and understand the instructions and provide the specification, not to implement it.

[the task you do].
The following sentence is a business requirement that the application must meet: ```{instructions}```

[output format].
Compile the business requirements into a concise list
Please separate the description into categories of business requirements, system requirements, and UI/UX design
[Important]
You are free to add to these specifications as you see fit
If you add more, you must be specific
""",
            "objective": f"""To document a clear and concise list of specifications for the {app_type}, derived from the given instructions.
This document will serve as the basis for developing a Minimum Viable Product (MVP), ensuring that the development focuses on essential features required for the initial launch.
""",
            "reason": """Establishing a clear set of specifications for the MVP is crucial to guide the development process efficiently and effectively.
By focusing on minimal requirements, resources can be optimally allocated to deliver a product that meets the core objectives, facilitating quicker iterations and feedback cycles.
This approach helps in validating the product concept with the least amount of effort and investment.
""",
        }
    ]
    return additional_tasks
