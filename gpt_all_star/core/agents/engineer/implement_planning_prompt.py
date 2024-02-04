from langchain_core.prompts import PromptTemplate

implement_planning_template = PromptTemplate.from_template(
    """Your task is as follows.
**IMPORTANT**: Your answer must be the full source code, only the source code and nothing else.
```
TODO: {todo_description}
GOAL: {todo_goal}
```

{finished_todo_message}

---
Represent files like so:

./PATH/FILENAME
```
CODE
```

The following tokens must be replaced like so:
PATh is a relative path to the file from the root directory of the project.
FILENAME is the lowercase combined path and file name including the file extension and **if the file already exists, please follow its name**.
CODE is the code in the file

Example representation of a file:

./src/index.js
```
ReactDOM.render(
    <React.StrictMode>
        <ChakraProvider>
            <App />
        </ChakraProvider>
    </React.StrictMode>,
    document.getElementById('root')
);
```
"""
)
