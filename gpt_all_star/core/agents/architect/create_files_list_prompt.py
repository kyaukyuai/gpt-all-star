from langchain_core.prompts import PromptTemplate

create_files_list_template = PromptTemplate.from_template(
    """Read and understand the specifications to build the application, technologies used to build the application and page URLs required by the application.

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

Thoughtfully determine and list the exact file names that the development team will create for the application.
There's no need to provide a description for each file.
Refrain from providing personal opinions or alternatives, only list the exact file names.
**Follow a language and framework appropriate best practice file naming convention.**
**Ensure all necessary files are accounted for.**
**The output should be presented in markdown format.**

FILENAME.md
```
CONTENT
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
CONTENT is the text in the file

Example representation of a file:

file.md
```
- ./hello_world.py
- ./model/user.py
```
"""
)
