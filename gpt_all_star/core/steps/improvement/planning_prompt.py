from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan to fully meet the user's requirements.

# Constraints
---
Must always fulfill the user's request exactly.
## request

```plaintext
{request}
```

# Current implementation
---
{current_source_code}
"""
)
