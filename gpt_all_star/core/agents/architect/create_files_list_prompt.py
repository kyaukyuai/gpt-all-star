from langchain_core.prompts import PromptTemplate

create_files_list_template = PromptTemplate.from_template(
    """Your task is to make sure you have an exhaustive list of all file names needed for the application.
**IMPORTANT**: Follow a language and framework appropriate best practice file naming convention.
**IMPORTANT**: Descriptions for each file name are not required, only provide the exact file path and file name.
**IMPORTANT**: Avoid providing personal opinions or alternatives.

{format}

Example representation of a file:

files.md
```
- ./public/index.html
- ./src/App.js
```
"""
)
