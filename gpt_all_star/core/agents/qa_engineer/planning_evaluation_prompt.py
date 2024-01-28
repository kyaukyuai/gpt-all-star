from langchain_core.prompts import PromptTemplate

planning_evaluation_template = PromptTemplate.from_template(
    """Your task is to devise a comprehensive plan for looking over the source code to insure that it is complete and does the job that it is supposed to do.

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
