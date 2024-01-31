from langchain_core.prompts import PromptTemplate

planning_ui_design_template = PromptTemplate.from_template(
    """Your task is to develop a detailed strategy for enhancing the UI and UX, taking full advantage of chakra-ui's features.

There are the specifications to build the application:
```
{specifications}
```

These are the current source code files:
```
{codes}
```

**IMPORTANT**: You must respond with ONLY the JSON object, with NO additional text or explanation.
**IMPORTANT**: Do not use ``` in your response.

Here is the schema for the expected JSON object:
```
{json_format}
```

Examples:
```
{example}
```
"""
)
