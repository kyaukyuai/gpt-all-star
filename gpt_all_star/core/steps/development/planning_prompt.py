from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan from project creation to source code implementation in order to build a fully working application.

# Constraints
---
- Verification of operation, deployment, and version control are done in separate steps and are not included in the development plan.
- Focus only on implementing source code that works perfectly according to the specification.

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

# Architecture
---
```system_architecture.md
{system_architecture}
```

# UI Design
---
```design_000.html
{design_html}
```
"""
)
