from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan from project creation to source code implementation in order to build a fully working application.

# Constraints
---
- The application specifications must be carefully understood and accurately reflected in the application.
- The operation check itself is performed in a separate step and is not included in the plan.

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
"""
)
