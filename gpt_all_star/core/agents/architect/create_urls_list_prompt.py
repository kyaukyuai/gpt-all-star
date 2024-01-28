from langchain_core.prompts import PromptTemplate

create_urls_list_template = PromptTemplate.from_template(
    """Your task is to consider carefully and list only the page URLs that are needed for the application.
**IMPORTANT**: Descriptions for each page URL are not required, only provide the exact page URL.
**IMPORTANT**: Avoid providing personal opinions or alternatives.

There are the specifications to build the application:
```
{specifications}
```

{format}

Example representation of a file:

pages.md
```
- localhost:3000/
```
"""
)
