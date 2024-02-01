from langchain_core.prompts import PromptTemplate

planning_improvement_template = PromptTemplate.from_template(
    """Your job is to create a detailed and specific plan to fully meet the user's requirements based on the current application specifications and source code.

Here is the request:
```
{request}
```

There are the current specifications to build the application:
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
