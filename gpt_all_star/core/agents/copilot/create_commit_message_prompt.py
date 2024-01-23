from langchain_core.prompts import PromptTemplate

create_commit_message_template = PromptTemplate.from_template(
    """Generate an appropriate commit message showing the following diffs.
The format should follow Conventional Commits.

Here is the diff:
```
{diff}
```
"""
)
