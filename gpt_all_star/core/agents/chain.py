from __future__ import annotations

import os

from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder

from gpt_all_star.core.agents.agent import Agent
from gpt_all_star.core.llm import LLM_TYPE, create_llm

ACTIONS = [
    "Execute a command",
    "Add a new file",
    "Read and Overwrite an existing file",
    "Delete an existing file",
]


class Chain:
    def __init__(self) -> None:
        self._llm = create_llm(LLM_TYPE[os.getenv("ENDPOINT", default="OPENAI")])

    def create_supervisor_chain(self, members: list[Agent] = []):
        members = [member.role.name for member in members]
        options = ["FINISH"]
        options.extend(members)
        system_prompt = f"""You are a supervisor tasked with managing a conversation between the following workers: {str(members)}.
Given the following user request, respond with the worker to act next.
Each worker will perform a task and respond with their results and status.
When finished, respond with FINISH.
"""
        function_def = {
            "name": "route",
            "description": "Select the next role.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "next": {
                        "title": "Next",
                        "anyOf": [
                            {"enum": options},
                        ],
                    }
                },
                "required": ["next"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}",
                ),
            ]
        ).partial(options=str(options))

        return (
            prompt
            | self._llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )

    def create_assign_supervisor_chain(self, members: list[Agent] = []):
        members = [member.role.name for member in members]
        system_prompt = f"""You are a supervisor tasked with managing a conversation between the following workers: {str(members)}.
Given the following user request, respond with the worker to act next.
Each worker will perform a task and respond with their results and status.
"""
        function_def = {
            "name": "assign",
            "description": "Assign the task.",
            "parameters": {
                "title": "routeSchema",
                "type": "object",
                "properties": {
                    "assign": {
                        "title": "Assign",
                        "anyOf": [
                            {"enum": members},
                        ],
                    }
                },
                "required": ["assign"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, who should act next?"
                    " Select one of: {members}",
                ),
            ]
        ).partial(members=str(members))

        return (
            prompt
            | self._llm.bind_functions(functions=[function_def], function_call="assign")
            | JsonOutputFunctionsParser()
        )

    def create_planning_chain(self, profile: str = ""):
        system_prompt = f"""{profile}
Based on the user request provided, your task is to generate a detail and specific plan that includes following items:
    - action: it must be one of {", ".join(ACTIONS)}
    - working_directory: a directory where the command is to be executed or the file is to be placed, it should be started from '.', e.g. './src'
    - filename: specify only if the name of the file to be added or changed is specifically determined
    - command: command to be executed if necessary
    - context: all contextual information that should be communicated to the person performing the task

Make sure that each step has all the information needed.
"""
        function_def = {
            "name": "planning",
            "description": "Create the plan.",
            "parameters": {
                "title": "planSchema",
                "type": "object",
                "properties": {
                    "plan": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "description": "Task to do.",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "description": "Task",
                                    "anyOf": [
                                        {"enum": ACTIONS},
                                    ],
                                },
                                "working_directory": {
                                    "type": "string",
                                    "description": "Directory where the command is to be executed or the file is to be located, it should be started from '.', e.g. './src'",
                                },
                                "filename": {
                                    "type": "string",
                                    "description": "Specify only if the name of the file to be added or changed is specifically determined",
                                },
                                "command": {
                                    "type": "string",
                                    "description": "Command to be executed if necessary",
                                },
                                "context": {
                                    "type": "string",
                                    "description": "All contextual information that should be communicated to the person performing the task",
                                },
                            },
                        },
                    }
                },
                "required": ["plan"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    """
Given the conversation above, create a detailed and specific plan to fully meet the user's requirements."
""",
                ),
            ]
        ).partial()

        return (
            prompt
            | self._llm.bind_functions(
                functions=[function_def], function_call="planning"
            )
            | JsonOutputFunctionsParser()
        )

    def create_replanning_chain(self, profile: str = ""):
        system_prompt = f"""{profile}
Based on the user request provided and the current implementation, your task is to update the original plan that includes following items:
    - action: it must be one of {", ".join(ACTIONS)}
    - working_directory: a directory where the command is to be executed or the file is to be placed, it should be started from '.', e.g. './src'
    - filename: specify only if the name of the file to be added or changed is specifically determined
    - command: command to be executed if necessary
    - context: all contextual information that should be communicated to the person performing the task

If no more steps are needed and you can return to the user, then respond with that.
Otherwise, fill out the plan.
"""
        function_def = {
            "name": "replanning",
            "description": "Create the replan.",
            "parameters": {
                "title": "planSchema",
                "type": "object",
                "properties": {
                    "plan": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "description": "Task to do.",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "description": "Task",
                                    "anyOf": [
                                        {"enum": ACTIONS},
                                    ],
                                },
                                "working_directory": {
                                    "type": "string",
                                    "description": "Directory where the command is to be executed or the file is to be located, it should be started from '.', e.g. './src'",
                                },
                                "filename": {
                                    "type": "string",
                                    "description": "Specify only if the name of the file to be added or changed is specifically determined",
                                },
                                "command": {
                                    "type": "string",
                                    "description": "Command to be executed if necessary",
                                },
                                "context": {
                                    "type": "string",
                                    "description": "All contextual information that should be communicated to the person performing the task",
                                },
                            },
                        },
                    }
                },
                "required": ["plan"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    """
Given the conversation above, update the original plan to fully meet the user's requirements."
""",
                ),
            ]
        ).partial()

        return (
            prompt
            | self._llm.bind_functions(
                functions=[function_def], function_call="replanning"
            )
            | JsonOutputFunctionsParser()
        )

    def create_git_commit_message_chain(self):
        system_prompt = "You are an excellent engineer. Given the diff information of the source code, please respond with the appropriate branch name and commit message for making the change."
        function_def = {
            "name": "commit_message",
            "description": "Information of the commit to be made.",
            "parameters": {
                "title": "commitMessageSchema",
                "type": "object",
                "properties": {
                    "branch": {
                        "type": "string",
                        "description": "Name of the branch to be pushed.",
                    },
                    "message": {
                        "type": "string",
                        "description": "Commit message to be used.",
                    },
                },
                "required": ["branch", "message"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, generate the appropriate branch name and commit message for making the change.",
                ),
            ]
        )

        return (
            prompt
            | self._llm.bind_functions(
                functions=[function_def], function_call="commit_message"
            )
            | JsonOutputFunctionsParser()
        )

    def create_command_to_execute_application_chain(self):
        system_prompt = "You are an excellent engineer. Given the source code, please respond with the appropriate command to execute the application."
        function_def = {
            "name": "execute_command",
            "description": "Command to execute the application",
            "parameters": {
                "title": "executeCommandSchema",
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "the command to execute the application",
                    },
                },
                "required": ["command"],
            },
        }
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "system",
                    "Given the conversation above, generate the command to execute the application",
                ),
            ]
        )

        return (
            prompt
            | self._llm.bind_functions(
                functions=[function_def], function_call="execute_command"
            )
            | JsonOutputFunctionsParser()
        )
