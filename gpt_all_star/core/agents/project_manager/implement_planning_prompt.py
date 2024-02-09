from langchain_core.prompts import PromptTemplate

implement_planning_template = PromptTemplate.from_template(
    """
# Instructions
---

While keeping track of the current status in the working directory, follow the TODO/DETAIL/WORKING_DIRECTORY to execute commands, add new files, or modify or delete existing files.
Check to see if the last GOAL has been met, and if so, exit; if not, continue working to meet it.

```
TODO: {todo}
DETAIL: {detail}
WORKING_DIRECTORY: {directory}
GOAL: {goal}
```

# Constraints
---
Must meet application specifications

# Specifications
---
```
{specifications}
```
"""
)
