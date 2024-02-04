from langchain_core.prompts import PromptTemplate

implement_planning_template = PromptTemplate.from_template(
    """Your task is as follows.
If you have already completed a TODO that you need to do, exit without outputting anything.
**IMPORTANT**: Make sure to use the full code when outputting the code.
```
TODO: {todo_description}
GOAL: {todo_goal}
```

{finished_todo_message}

---
Represent files like so:

FILENAME
```
CODE
```

The following tokens must be replaced like so:
FILENAME is the lowercase combined path and file name including the file extension and **if the file already exists, please follow its name**.
CODE is the code in the file

Example representation of a file:

./src/index.js
```
import React from 'react';
import ReactDOM from 'react-dom';
import { ChakraProvider } from '@chakra-ui/react';
import App from './App';

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
