from langchain_core.prompts import PromptTemplate

implement_planning_template = PromptTemplate.from_template(
    """
# Instructions
---

Conduct task: `{task}` with horizontal thinking according to context: `{context}`

# Constraints
---
Understand exactly why you should do: `{reason}` it and make sure you meet the status to be achieved: `{objective}`.

# Current implementation
---
```
{implementation}
```

# Specifications
---
```
{specifications}
```
"""
)
