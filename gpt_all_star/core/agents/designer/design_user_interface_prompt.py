from langchain_core.prompts import PromptTemplate

design_user_interface_template = PromptTemplate.from_template(
    """Analyze the specifications to built the application.

There are the specifications to build the application:
```
{specifications}
```

**Fix the UI and UX to be modern, stylish and fashionable like iPhone. Make the design eye-catching for everyone.**
**Do not change only the look and experience, but do not remove the functionality provided.**

Take requests for changes to the supplied code, and then you MUST
**1. (planning) Think step-by-step and explain the needed changes. Don't include *edit blocks* in this part of your response, only describe code changes.**
**2. (output) Describe each change per the example below.**

**You will output the content of each file necessary to achieve the goal, including ALL code.**
Always use best practices when coding.
When you edit or add code, respect and use existing conventions, libraries, etc.
**Do not comment on what every file does. Please note that the code should be fully functional. No placeholders.**
**Please note that the code should be fully functional. No placeholders.**

Follow a language and framework appropriate best practice file naming convention.
Make sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.
Ensure to implement all code, if you are unsure, write a plausible implementation.
Include module dependency or package manager dependency definition file.
Before you finish, double check that all parts of the architecture is present in the files.

Represent files like so:

FILENAME
```
CODE
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension and **if the file already exists, please follow its name**.
CODE is the code in the file

Example representation of a file:

./hello_world.py
```
print("Hello World")
```
"""
)
