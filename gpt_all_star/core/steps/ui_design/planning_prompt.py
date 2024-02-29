from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan to enhance the UI and UX in accordance with human interface guideline.

# Constraints
---
- Verification of operation, deployment, and version control are done in separate steps and are not included in the development plan.
- Focus only on implementing source code that works perfectly according to the specification.

# Current implementation
---
{current_source_code}

# Specifications
---
```specifications.md
{specifications}
```
"""
)
