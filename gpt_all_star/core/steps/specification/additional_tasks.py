def create_additional_tasks(app_type, instructions):
    additional_tasks = [
        {
            "action": "Add a new file",
            "working_directory": ".",
            "filename": "specifications.md",
            "command": "",
            "context": f"""The task is to clarify specifications of a {app_type}.
    Your role is to read and understand the instructions and provide the specifications, not to implement them.
    Please itemize the list of specifications inferred from the instructions.
    **IMPORTANT**: Please keep the specifications as minimal as possible to build our MVP (Minimum Viable Product).
    The following are requirements that your application must meet: ```{instructions}```
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
