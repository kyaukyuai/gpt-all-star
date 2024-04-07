def create_additional_tasks(app_type, instructions) -> list:
    additional_tasks = [
        {
            "action": "Add a new file",
            "working_directory": ".",
            "filename": "specifications.md",
            "command": "",
            "context": f"""The task is to clarify specifications of a {app_type} and provide the specifications document in markdown format, not to implement them.
The following is the instruction that the application must meet:
```
{instructions}
```

First, summarize the instructions into a list of concise bullet points that need further clarification.
Then, assume the ambiguity as the simplest possible specification for building the MVP(Minimum Viable Product) and state them clearly.
**IMPORTANT**: Please describe the specifications inferred from the instructions in as much detail as possible.

It must be included in the specifications document.
---
1. Product Overview
    Purpose of the product, target users, main features, etc.

2. Functional Requirements
    Details of specific functions the product should provide
    Priority and importance of each function

3. Non-functional Requirements
    Quality requirements such as performance, security, usability, reliability, etc.
    Supported platforms, devices, operating systems, etc.
    NOT include technical requirements

4. Glossary
    Explanation of technical terms and abbreviations used in the specification document
""",
        }
    ]
    return additional_tasks
