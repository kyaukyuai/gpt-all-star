from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan from project creation to source code implementation, testing, and operation verification in order to build a correctly working application.

# Constraints
---
- The application specifications must be carefully understood and accurately reflect the specifications.
- Finally, create `run.sh`, a bash script to automate the setup and execution processes within the project without needing global installations or superuser privileges.

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
