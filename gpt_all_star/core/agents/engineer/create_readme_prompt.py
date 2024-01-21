from langchain_core.prompts import PromptTemplate

create_readme_template = PromptTemplate.from_template(
    """You will get information about a codebase and documents that are currently on disk in the current folder.
Please create README.md file.
It should contain the following information:
- A project title
- A brief description of the project
- technology stack
- requirements
- how to run the project

You will output the content to achieve the goal.
Represent files like so:

FILENAME
```
CONTENT
```

The following tokens must be replaced like so:
FILENAME must be `README.md`.
CONTENT is the content in the file

Example representation of a file:

README.md
```
# project title
```
"""
)
