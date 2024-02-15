from langchain_core.prompts import PromptTemplate

"""Represents a prompt template for creating a detailed and specific development plan based on the given error.

This template is used to generate development plans for rectifying errors. It includes instructions, constraints, the error message, and the current implementation snippet.
"""
planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan to rectify the following errors.

# Constraints
---
Understand the exact error wording and be sure to correct it.

## Error
```
{error}
```

# Current implementation
---
```
{current_source_code}
```
"""
)
