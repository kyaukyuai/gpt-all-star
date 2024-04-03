from langchain_core.prompts import PromptTemplate

replanning_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan from project creation to source code implementation in order to build a correctly working application.

# Original plan was this:
---
{original_plan}

# You have currently done the follow tasks:
---
{completed_plan}

# Current implementation
---
{implementation}

# Constraints
---
- Verification of operation, deployment, and version control are done in separate steps and are not included in the development plan.
- Focus only on implementing source code that works perfectly according to the requirements.

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
