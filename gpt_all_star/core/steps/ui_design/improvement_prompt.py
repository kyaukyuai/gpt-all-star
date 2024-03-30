from langchain_core.prompts import PromptTemplate

improvement_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Update ui_design.html to fully satisfy the user's request.

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

## UI Design
```ui_design.html
{ui_design}
```
"""
)
