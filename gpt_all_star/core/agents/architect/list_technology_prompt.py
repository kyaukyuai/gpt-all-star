from langchain_core.prompts import PromptTemplate

list_technology_template = PromptTemplate.from_template(
    """
Read and understand the specifications.

Here is specifications:
```
{specifications}
```

Think step by step and list only the name of technologies that the development team will use to build the application.
It is not necessary to give a description of each technology.
Do not give any subjective thoughts or options, give exact technologies.
**Technologies related to source code implementation should be listed, not version control tools, technologies related to automated testing or deployment, or tools related to project management.**

Project Technology Guidelines

Relevance: Only include technologies that are essential and will be actively used in the project. Avoid mentioning any technologies that are not required.
Compatibility: Ensure that the listed technologies are compatible with each other. Exclude any technologies that cannot be integrated or used in conjunction with others. For example, Pandas (Python library) and Node.js can't be used together. Another example is MongoDB (NoSQL database) and MySQL (SQL database) shouldn't be used together unless that is specified in project description.
Technology Preferences: In scenarios where multiple technology options are available for a specific project component, prioritize the following preferred technologies:

- Node.js
- SQLite OR MongoDB
- Bootstrap
- HTML
- CSS3
- Docker / Docker Compose

**The output should be presented in markdown format.**

FILENAME.md
```
CONTENT
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
CONTENT is the text in the file

Example representation of a file:

technologies.md
```
- Node.js
- SQLite OR MongoDB
- Bootstrap
- HTML
- CSS3
- Docker / Docker Compose
```
"""
)
