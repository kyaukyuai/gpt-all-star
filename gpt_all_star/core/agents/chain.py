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
        member_names = [member.role.name for member in members]
        profiles = "\n\n".join(
            f"{member.role.name}\n--\n{member.profile}" for member in members
        )
        options = ["FINISH"]
        options.extend(member_names)
        system_prompt = f"""You are a `Supervisor` tasked with managing a conversation between the following workers: {str(member_names)}.
Each member has a profile that describes their capabilities and specialties.
```
{profiles}
```
Each worker will perform a task and respond with their results and status.
Given the user request, determine the next worker to act or if the task is complete.
If the worker is prompted to finish like `Supervisor: FINISH`, always be answered with `FINISH`.
"""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        ).partial(options=str(options))

        class Next(BaseModel):
            next: str = Field(
                description=f"The next worker to act from members({str(member_names)}) or `FINISH` to finish the task"
            )

        def parse(message: Next) -> dict:
            next = (
                self.remove_quotes(message.next)
                if message and hasattr(message, "next")
                else "FINISH"
            )
            return {"next": next if next in member_names else "FINISH"}

        return prompt | self.llm.with_structured_output(Next) | parse

    def create_assign_supervisor_chain(self, members: list[Agent] = []):
        member_names = [member.role.name for member in members]
        profiles = "\n\n".join(
            f"{member.role.name}\n--\n{member.profile}" for member in members
        )
        system_prompt = f"""You are a `Supervisor` tasked with managing a conversation between the following workers: {str(member_names)}.
Each member has a profile that describes their capabilities and specialties.
```
{profiles}
```
Each worker will perform a task and respond with their results and status.
Given the following user request, respond with the worker to act next.
"""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
                (
                    "human",
                    "Given the conversation above, who should act next?"
                    " Select one of: {member_names}",
                ),
            ]
        ).partial(member_names=str(member_names))

        class Assign(BaseModel):
            assign: str = Field(
                description=f"The worker to assign the task from members({str(member_names)})"
            )

        def parse(message: Assign) -> dict:
            assign = (
                self.remove_quotes(message.assign)
                if message and hasattr(message, "assign")
                else "PROJECT_MANAGER"
            )
            return {"assign": assign if assign in member_names else "PROJECT_MANAGER"}

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
            try:
                return {"plan": ai_message.tool_calls[0]["args"]["plan"]}
            except (KeyError, IndexError):
                return {"plan": []}

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
            try:
                return {"plan": ai_message.tool_calls[0]["args"]["plan"]}
            except (KeyError, IndexError):
                return {"plan": []}

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
