from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Review current implementation and develop a detailed plan to correct areas that are not as per requirements.

# Constraints
---
- `working_directory` is very important, so please pay close attention!

# Current implementation
---
{current_source_code}

# Requirements
---

## Application Specifications to be met

Application must be met with following specifications.

```specifications.md
{specifications}
```

## Technology requirements

Application must be built with following technology requirements.

```technologies.md
{technologies}
```

## UI Design to be implemented

Screen layout of the application must be same as following ui_design.

```ui_design.html
{ui_design}
```
"""
)
