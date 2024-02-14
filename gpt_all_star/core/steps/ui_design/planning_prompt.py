from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan to enhance the UI and UX in accordance with human interface guideline.

# Constraints
---
The application specifications must be carefully understood and accurately reflect the specifications.

# Current implementation
---
```
{current_source_code}
```

# Specifications
---
```
{specifications}
```
"""
)
