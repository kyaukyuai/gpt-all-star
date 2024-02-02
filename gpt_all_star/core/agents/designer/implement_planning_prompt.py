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

**IMPORTANT**: If you have already implemented a TODO that you need to do, exit without outputting anything.
**IMPORTANT**: Make sure to use the full code when outputting the code.

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
