from langchain_core.prompts import PromptTemplate

improvement_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Based on the current situation, create a detailed and specific development plan to fully meet the user request.

# Constraints
---
Must always fulfill the user's request exactly.

# Request
---
```plaintext
{request}
```

# Current Situation
---

## Current implementation
{current_source_code}
"""
)
