from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan from project creation to source code implementation, testing, and operation verification in order to build a correctly working application.

# Constraints
---
- The application specifications must be carefully understood and accurately reflect the specifications.
- Start from `npx create-react-app app`

# Requirements
---

## Application Specifications to be met
```
{specifications}
```

## Technology stack to be used
```
{technologies}
```

## Page URL to be implemented
```
{pages}
```

## Files to be implemented
```
{files}
```
"""
)
