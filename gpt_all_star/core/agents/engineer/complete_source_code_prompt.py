from langchain_core.prompts import PromptTemplate

complete_source_code_template = PromptTemplate.from_template(
    """Your task is to find the file with implementation omissions and correct them to a complete implementation.
In particular, if any of the following wording is found in the file, it needs to be corrected.
- will go here
- will be added here
- PlaceHolder
- TODO

```
{codes}
```

You will output the content of each file necessary to achieve the goal, including ALL code.
**IMPORTANT**: Final answer must be the full codes, only the codes and nothing else.
**IMPORTANT**: Never use placeholders!

Represent files like so:

FILENAME
```
CODE
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension and **if the file already exists, please follow its name**.
CODE is the code in the file

Example representation of a file:

./hello_world.py
```
print("Hello World")
"""
)
