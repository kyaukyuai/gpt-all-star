from langchain_core.prompts import PromptTemplate

create_urls_list_template = PromptTemplate.from_template(
    """Your task is to list only the page URLs that are needed for the application.
There is no need to provide a description for each page URL.
Avoid providing personal opinions or alternatives, only provide the exact page URLs.

There are the specifications to build the application:
```
{specifications}
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

pages.md
```
- localhost:3000/
```
"""
)
