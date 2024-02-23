from langchain_core.prompts import PromptTemplate

planning_prompt_template = PromptTemplate.from_template(
    """
# Instructions
---
Create a detailed and specific development plan to create `run.sh` script to automate the setup and execution processes within the project.

# Constraints
---
- The run.sh script is created to automate the setup and execution processes within the project without needing global installations or superuser privileges.
- The script encapsulates commands for locally installing dependencies, setting environment variables, and starting necessary parts of the codebase in parallel.
- It must adhere to security best practices and be based on project-specific requirements.

# Current implementation
---
{current_source_code}
"""
)
