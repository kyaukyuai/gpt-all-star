from langchain_core.prompts import PromptTemplate

implement_planning_template = PromptTemplate.from_template(
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
