from langchain_core.prompts import PromptTemplate

planning_ui_design_template = PromptTemplate.from_template(
    """Your task is to create a detailed and specific plan to enhance the UI and UX in accordance with human interface guideline, using the information provided.

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
