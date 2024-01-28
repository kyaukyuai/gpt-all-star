from langchain_core.prompts import PromptTemplate

create_files_list_template = PromptTemplate.from_template(
    """Your task is to consider carefully and make an exhaustive list of all file names required for the application.
**IMPORTANT**: Follow a language and framework appropriate best practice file naming convention.
**IMPORTANT**: Descriptions for each file name are not required, only provide the exact file path and file name.
**IMPORTANT**: Avoid providing personal opinions or alternatives.

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

{format}

Example representation of a file:

files.md
```
- ./hello_world.py
- ./model/user.py
```
"""
)
