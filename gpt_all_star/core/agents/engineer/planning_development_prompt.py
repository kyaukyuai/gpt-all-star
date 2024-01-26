from langchain_core.prompts import PromptTemplate

planning_development_prompt_template = PromptTemplate.from_template(
    """Your task is to devise a comprehensive plan for generating complete Python code to construct the application.

Analyze the specifications, technologies, pages, and files required to build the application.

There are the specifications to build the application:
```
{specifications}
```

These are the technologies used to build the application
```
{technology}
```

These are the page URLs required by the application:
```
{page}
```

These are the files required by the application:
```
{file}
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
