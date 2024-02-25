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
- The application specifications must be carefully understood and accurately reflect the specifications.
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
