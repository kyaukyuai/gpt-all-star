from langchain_core.prompts import PromptTemplate

planning_healing_template = PromptTemplate.from_template(
    """Your task is to create a detailed and specific plan to rectify the following errors, using the information provided.
Only critical errors should be resolved, ignore warnings.

There are the errors occurred when run the application:
```
{errors}
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
