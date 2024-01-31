from langchain_core.prompts import PromptTemplate

create_technologies_list_template = PromptTemplate.from_template(
    """Your task is to consider carefully and list the exact techniques for building an application with the following specifications.
**IMPORTANT**: Only technologies related to source code implementation should be listed, not version control tools, technologies related to automated testing or deployment, or tools related to project management.
**IMPORTANT**: List only the minimum required technology.
**IMPORTANT**: Descriptions for each technology are not required, only provide the exact technology name.
**IMPORTANT**: Avoid providing personal opinions or alternatives.

There are the specifications to build the application:
```
{specifications}
```

Technologies Guidelines
```
Relevance: Only include technologies that are essential and will be actively used in the project. Avoid mentioning any technologies that are not required.
Compatibility: Ensure that the listed technologies are compatible with each other. Exclude any technologies that cannot be integrated or used in conjunction with others. For example, Pandas (Python library) and Node.js can't be used together. Another example is MongoDB (NoSQL database) and MySQL (SQL database) shouldn't be used together unless that is specified in project description.
Preferences: In scenarios where multiple technology options are available for a specific project component, prioritize the following preferred technologies.

- React
- JavaScript
- chakra-ui
- HTML
- Docker / Docker Compose
```

{format}

Example representation of a file:

technologies.md
```
- React
- JavaScript
- chakra-ui
- HTML
- Docker / Docker Compose
```
"""
)
