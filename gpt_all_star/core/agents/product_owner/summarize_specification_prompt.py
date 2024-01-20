from langchain_core.prompts import PromptTemplate

summarize_specifications_template = PromptTemplate.from_template(
    """Based on what we have discussed so far, please summarize the specifications of our software application.
**Please be as detailed as possible so that engineers will have no difficulty in implementing the software application.**
**The output should be presented in markdown format.**

FILENAME
```
SPECIFICATION
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension.
SPECIFICATION is the text in the file.

Example representation of a file:

specification.md
```
# Outline
```
"""
)
