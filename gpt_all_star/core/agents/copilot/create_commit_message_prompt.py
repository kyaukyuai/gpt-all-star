from langchain_core.prompts import PromptTemplate

create_commit_message_template = PromptTemplate.from_template(
    """Generate an appropriate branch name and commit message showing the following diffs.
The format should follow Conventional Commits.

Here is the diff:
```
{diff}
```

**IMPORTANT**: You must respond with ONLY the JSON object, with NO additional text or explanation.
**IMPORTANT**: Do not use ``` in your response.

Here is the schema for the expected JSON object:
```
{json_format}
```

Examples:
```
{example}
```
"""
)
