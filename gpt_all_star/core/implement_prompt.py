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
Understand exactly why you should do it and make sure you meet the status to be achieved.
- reason: {reason}
- objective: {objective}

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

## Files to be implemented
```files.md
{files}
```
"""
)
