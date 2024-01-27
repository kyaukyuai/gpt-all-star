from langchain_core.prompts import PromptTemplate

clarify_instructions_template = PromptTemplate.from_template(
    """The task is to clarify specifications of a {app_type}.
Your role is to read and understand the instructions, not to implement them.
**IMPORTANT**: First, summarize the instructions into a list of concise bullet points that need further clarification.
**IMPORTANT**: Then, select one point from the list and ask a clarifying question to the user.

There are the instructions to build the application:
```
{instructions}
```
"""
)

auto_clarify_instructions_template = PromptTemplate.from_template(
    """The task is to clarify specifications of a {app_type}.
Your role is to read and understand the instructions and provide the specifications, not to implement them.
Please itemize the list of specifications inferred from the instructions.
**IMPORTANT**: Please keep the specifications as minimal as possible to build our MVP(Minimum Viable Product).

There are the instructions to build the application:
```
{instructions}
```
"""
)
