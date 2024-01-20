from langchain_core.prompts import PromptTemplate

clarify_instructions_template = PromptTemplate.from_template(
    """The task is to develop an application of type {app_type}.
Your role is to read and understand the instructions, not to implement them.
**First, summarize the instructions into a list of concise bullet points that need further clarification.**
**Then, select one point from the list and ask a clarifying question to the user.**

Here are the instructions:
```
{instructions}
```
"""
)
