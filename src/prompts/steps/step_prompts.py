# CLARIFY
from langchain_core.prompts import PromptTemplate

clarify_instructions_template = PromptTemplate.from_template("""
You will read instructions and not carry them out, only seek to clarify them.
Specifically you will first summarise a list of super short bullets of areas that need clarification.
Then you will pick one clarifying question, and wait for an answer from the user.

Here is the instructions:
```
{instructions}
```
""")

summarize_specifications_template = PromptTemplate.from_template("""
Please summarize the specifications of the software application based on the conversations we have had,
to be developed in such a way that the engineer will have no difficulty in implementing the software application.
The output should be presented in markdown format.

FILENAME
```
SPECIFICATION
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
SPECIFICATION is the text in the file

Example representation of a file:

specification.md
```
# Outline
```
""")
