from __future__ import annotations

import os

from langchain_core.messages.ai import AIMessage
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.pydantic_v1 import BaseModel, Field

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
        self.llm_type = LLM_TYPE[os.getenv("ENDPOINT", default="OPENAI")]
        self.llm = create_llm(self.llm_type)

    @staticmethod
    def remove_quotes(string):
        if string.startswith("'") and string.endswith("'"):
            return string[1:-1]
        return string

    def create_supervisor_chain(self, members: list[Agent] = []):
        members = [member.role.name for member in members]
        options = ["FINISH"]
        options.extend(members)
        system_prompt = f"""You are a supervisor tasked with managing a conversation between the following workers: {str(members)}.
Given the following user request, respond with the worker to act next.
Each worker will perform a task and respond with their results and status.
When finished, respond with FINISH.
"""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "human",
                    "Given the conversation above, who should act next?"
                    " Or should we FINISH? Select one of: {options}",
                ),
            ]
        ).partial(options=str(options))

        class Next(BaseModel):
            next: str = Field(description="The next role to act")

        def parse(message: Next) -> dict:
            return {"next": self.remove_quotes(message.next)}

        return prompt | self.llm.with_structured_output(Next) | parse

    def create_assign_supervisor_chain(self, members: list[Agent] = []):
        members = [member.role.name for member in members]
        system_prompt = f"""You are a supervisor tasked with managing a conversation between the following workers: {str(members)}.
Given the following user request, respond with the worker to act next.
Each worker will perform a task and respond with their results and status.
"""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "human",
                    "Given the conversation above, who should act next?"
                    " Select one of: {members}",
                ),
            ]
        ).partial(members=str(members))

        class Assign(BaseModel):
            assign: str = Field(description="The role to assign the task")

        def parse(message: Assign) -> dict:
            return {"assign": self.remove_quotes(message.assign)}

        return prompt | self.llm.with_structured_output(Assign) | parse

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
        tool_def = {
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
                    "human",
                    """
Given the conversation above, create a detailed and specific plan to fully meet the user's requirements."
""",
                ),
            ]
        ).partial()

        def parse(ai_message: AIMessage) -> dict:
            return {"plan": ai_message.tool_calls[0]["args"]["plan"]}

        return prompt | self.llm.bind_tools([tool_def]) | parse

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
        tool_def = {
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
                    "human",
                    """
Given the conversation above, update the original plan to fully meet the user's requirements."
""",
                ),
            ]
        ).partial()

        def parse(ai_message: AIMessage) -> dict:
            return {"plan": ai_message.tool_calls[0]["args"]["plan"]}

        return prompt | self.llm.bind_tools([tool_def]) | parse

    def create_git_commit_message_chain(self):
        system_prompt = "You are an excellent engineer. Given the diff information of the source code, please respond with the appropriate branch name and commit message for making the change."
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "human",
                    "Given the conversation above, generate the appropriate branch name and commit message for making the change.",
                ),
            ]
        )

        class CommitMessage(BaseModel):
            branch: str = Field(description="The branch name to use")
            message: str = Field(description="The commit message to use")

        def parse(message: CommitMessage) -> dict:
            return {"branch": message.branch, "message": message.message}

        return prompt | self.llm.with_structured_output(CommitMessage) | parse

    def create_command_to_execute_application_chain(self):
        system_prompt = "You are an excellent engineer. Given the source code, please respond with the appropriate command to execute the application."
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "human",
                    "Given the conversation above, generate the command to execute the application",
                ),
            ]
        )

        class ExecuteCommand(BaseModel):
            command: str = Field(description="The command to execute the application")

        def parse(message: ExecuteCommand) -> dict:
            return {"command": message.command}

        return prompt | self.llm.with_structured_output(ExecuteCommand) | parse
