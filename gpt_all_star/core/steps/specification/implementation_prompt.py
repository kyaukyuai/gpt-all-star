from langchain_core.prompts import PromptTemplate

implementation_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Conduct `task` with horizontal thinking according to `context`.
Inform the `Supervisor` to respond with `FINISH` if the task has been completed successfully.
You do not need to proceed with any subsequent tasks.

- task: {task}
- context: {context}
"""
)
