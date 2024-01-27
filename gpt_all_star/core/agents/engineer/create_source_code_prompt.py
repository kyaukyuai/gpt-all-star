from langchain_core.prompts import PromptTemplate

create_source_code_template = PromptTemplate.from_template(
    """Analyze the specifications, technologies, pages, and files required to build the application.

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

You will output the content of each file necessary to achieve the goal, including ALL code.
**Do not comment on what every file does. Please note that the code should be fully functional. No placeholders.**
**Please note that the code should be fully functional. No placeholders.**

Follow a language and framework appropriate best practice file naming convention.
Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.
Ensure to implement all code, if you are unsure, write a plausible implementation.
Include module dependency or package manager dependency definition file.
Before you finish, double check that all parts of the architecture is present in the files.

Represent files like so:

FILENAME
```
CODE
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
CODE is the code in the file
**Be sure to include all codes without omission!**

Example representation of a file:

./hello_world.py
```
print("Hello World")
```
"""
)
