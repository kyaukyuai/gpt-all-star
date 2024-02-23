from langchain_core.prompts import PromptTemplate

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
{current_source_code}
"""
)
