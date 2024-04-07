from langchain_core.prompts import PromptTemplate

implement_template = PromptTemplate.from_template(
    """
# Instructions
---
Conduct `task` with horizontal thinking according to `context`.
- task: {task}
- context: {context}

# Constraints
---
- Please check the contents of the directories and files of the current implementation before executing the task.

# Current implementation
---
{implementation}

# Requirements
---

## Application Specifications to be met
```specifications.md
{specifications}
```

## Technology stack to be used
```technologies.md
{technologies}
```

## UI Design to be implemented
```ui_design.html
{ui_design}
```
"""
)
