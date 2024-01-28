from langchain_core.prompts import PromptTemplate

implement_planning_prompt_template = PromptTemplate.from_template(
    """We've broken down the plan into {num_of_todo} TODOs.
```
{todo_list}
```

You are currently working on TODO{index_of_todo} with the following description:
```
{todo_description}
```

{finished_todo_message}
After a TODO is finished, please make sure you meet the goal: {todo_goal}.
If you have already implemented a TODO that you need to do, exit without outputting anything.

You will output the content of each file necessary to achieve the goal, including ALL code.
**IMPORTANT**: Final answer must be the full codes, only the codes and nothing else.
**IMPORTANT**: Never use placeholders!
For Python, you always create an appropriate requirements.txt file.
For NodeJS, you always create an appropriate package.json file.

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
