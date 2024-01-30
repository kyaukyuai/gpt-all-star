from langchain_core.prompts import PromptTemplate

planning_evaluation_template = PromptTemplate.from_template(
    """Your task is to look through the source code and create a detailed plan to check for and correct implementation omissions, import errors, and syntax errors.

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
