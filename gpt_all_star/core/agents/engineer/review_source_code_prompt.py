from langchain_core.prompts import PromptTemplate

review_source_code_template = PromptTemplate.from_template(
    """We've broken down the plan into {num_of_todo} TODOs.
```
{todo_list}
```

We have just finished TODO{index_of_todo} with the following description:
```
todo: {todo_description}
goal: {todo_goal}
```

{finished_todo_message}
Your task is to review that {todo_review} to make sure it is correct and meets the goal.
If there are no problems after reviewing, exit without outputting anything.
Your Final answer must be the full code, only the python code and nothing else.

Represent files like so:

FILENAME
```
CODE
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension and **if the file already exists, please follow its name**.
CODE is the code in the file
**Be sure to include all codes without omission!**

Example representation of a file:

./hello_world.py
```
print("Hello World")
```
"""
)
