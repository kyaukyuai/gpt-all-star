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

generate_sourcecode_template = PromptTemplate.from_template("""
You will read specifications and think step by step and reason yourself to the correct decisions to make sure we get it right.
First lay out the names of the core classes, functions, methods that will be necessary, As well as a quick comment on their purpose.

Here is the specifications:
```
{specifications}
```

You will output the content of each file necessary to achieve the goal, including ALL code.
Represent files like so:

FILENAME
```
CODE
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension
CODE is the code in the file

Example representation of a file:

src/hello_world.py
```
print("Hello World")
```

Do not comment on what every file does. Please note that the code should be fully functional. No placeholders.

**Please note that the code should be fully functional. No placeholders.**

Follow a language and framework appropriate best practice file naming convention.
Make sure that files contain all imports, types etc.  The code should be fully functional. Make sure that code in different files are compatible with each other.
Ensure to implement all code, if you are unsure, write a plausible implementation.
Include module dependency or package manager dependency definition file.
Before you finish, double check that all parts of the architecture is present in the files.

When you are done, write finish with "this concludes a fully working implementation".
""")

generate_entrypoint_template = PromptTemplate.from_template("""
You will get information about a codebase that is currently on disk in the current folder.
From this you will answer with code blocks that includes all the necessary unix terminal commands to
a) install dependencies
b) run all necessary parts of the codebase (in parallel if necessary).
Do not install globally. Do not use sudo.
Do not explain the code, just give the commands.
Do not use placeholders, use example values (like . for a folder argument) if necessary."
""")
