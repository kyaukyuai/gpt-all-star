from langchain_core.prompts import PromptTemplate

planning_development_template = PromptTemplate.from_template(
    """Your task is to create a detailed and specific plan for writing the full code necessary to build the application, using the information provided.

There are the specifications to build the application:
```
{specifications}
```

These are the technologies used to build the application
```
{technologies}
```

These are the page URLs required by the application:
```
{pages}
```

These are the files required by the application:
```
{files}
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
