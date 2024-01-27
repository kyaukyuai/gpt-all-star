from langchain_core.prompts import PromptTemplate

list_page_template = PromptTemplate.from_template(
    """Read and understand the specifications to build the application.

There are the specifications to build the application:
```
{specifications}
```

Carefully consider and list only the page URLs that the development team needs to construct.
Avoid providing personal opinions or alternatives, only provide the exact URLs.

**The output should be presented in markdown format.**

FILENAME.md
```
CONTENT
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
CONTENT is the text in the file

Example representation of a file:

pages.md
```
- localhost:3000/
```
"""
)
