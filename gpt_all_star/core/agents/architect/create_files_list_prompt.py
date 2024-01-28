from langchain_core.prompts import PromptTemplate

create_files_list_template = PromptTemplate.from_template(
    """Your task is to make an exhaustive list of all file names required for the application.
Follow a language and framework appropriate best practice file naming convention.
There is no need to provide a description for each file names.
Avoid providing personal opinions or alternatives, only provide the exact file names.

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

**IMPORTANT**: The output should be presented in markdown format.

FILENAME.md
```
CONTENT
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
CONTENT is the text in the file

Example representation of a file:

files.md
```
- ./hello_world.py
- ./model/user.py
```
"""
)
