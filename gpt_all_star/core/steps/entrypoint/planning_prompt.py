from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan to create `run.sh` script to automate the setup and execution processes within the project.

# Constraints
---
- The `run.sh` script is created to automate the setup and execution processes within the project without needing global installations or superuser privileges.
- Check the current implementation and directory structure and be sure to launch the application.
- Do not use docker and docker-compose.
- Do not include tests in the script.

# Current implementation
---
{current_source_code}
"""
)
