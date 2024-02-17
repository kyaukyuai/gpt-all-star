from __future__ import annotations

import os
import re
from abc import ABC
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
from typing import Optional

import openai
from langchain.agents.agent import AgentExecutor
from langchain.agents.agent_toolkits.file_management.toolkit import (
    FileManagementToolkit,
)
from langchain.agents.openai_tools.base import create_openai_tools_agent
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from rich.markdown import Markdown
from rich.panel import Panel

from gpt_all_star.cli.console_terminal import ConsoleTerminal
from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.tools.shell_tool import ShellTool

# from gpt_all_star.core.tools.llama_index_tool import llama_index_tool
from gpt_all_star.helper.text_parser import format_file_to_input

NEXT_COMMAND = "next"

ACTIONS = [
    "Execute a command",
    "Add a new file",
    "Read and Overwrite an existing file",
    "Delete an existing file",
]


class Agent(ABC):
    def __init__(
        self,
        role: AgentRole,
        storages: Storages | None,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
        color: str | None = None,
        tools: list = [],
    ) -> None:
        self.console = ConsoleTerminal()
        self._llm = _create_llm(os.getenv("OPENAI_API_MODEL_NAME"), 0.1)

        self.role: AgentRole = role
        self.name: str = name or self._get_default_profile().name
        self.profile: str = profile or self._get_default_profile().prompt.format()
        self.color: str = color or self._get_default_profile().color

        self.messages: list[BaseMessage] = [Message.create_system_message(self.profile)]
        self.storages = storages
        self.debug_mode = debug_mode

        working_directory = (
            self.storages.app.path.absolute() if self.storages else os.getcwd()
        )
        file_tools = FileManagementToolkit(
            root_dir=str(working_directory),
            selected_tools=["read_file", "write_file", "list_directory", "file_delete"],
        ).get_tools()
        self.tools = (
            tools
            + file_tools
            + [ShellTool(verbose=True, root_dir=str(working_directory))]
        )
        self.executor = self._create_executor(self.tools)

    def invoke(self, input: Optional[str] = None) -> None:
        if input is not None:
            self.messages.append(Message.create_human_message(input))

        callbacks = [StreamingStdOutCallbackHandler()] if self.debug_mode else []
        result = self.executor.invoke(
            {"messages": self.messages}, config={"callbacks": callbacks}
        )
        self.messages.append(Message.create_ai_message(result["output"]))

    def state(self, text: str) -> None:
        self.console.print(f"{self.name}: {text}", style=f"bold {self.color}")

    def output_md(self, md: str) -> None:
        self.console.print(Panel(Markdown(md, style="bold")))

    def ask(self, question: str, is_required: bool = True, default: str = None) -> str:
        while True:
            if default and default.endswith("\n"):
                default = re.sub(r"\n$", "", default)
            default_value = f"\n(default: {default})" if default else ""
            self.console.print(
                f"[{self.color} bold]{self.name}: {question}[/{self.color} bold][white]{default_value}[/white]"
            )
            answer = self.console.input("project.history").strip() or default
            self.console.new_lines(1)

            if answer or not is_required:
                return answer
            print("No input provided! Please try again.")

    def present_choices(
        self,
        question: str,
        choices: list[str],
        default: str,
    ) -> str:
        return self.console.choice(
            f"{self.name}: {question} (default: {default})",
            choices=choices,
            default=default,
            style=f"bold {self.color}",
        )

    def latest_message_content(self) -> str:
        return self.messages[-1].content.strip()

    def execute(
        self,
        follow_up_message: str,
        final_message: str | None = None,
        review_mode: bool = False,
    ) -> None:
        user_input = None
        count = 0

        while True:
            if count > 0:
                if not review_mode:
                    self._handle_final_message(final_message)
                    break

                self.console.new_lines(1)
                user_input = self.ask(follow_up_message)
                if user_input == NEXT_COMMAND:
                    self._handle_final_message(final_message)
                    break

            self.invoke(user_input)
            self.console.new_lines(1)
            count += 1

    def _handle_final_message(self, final_message: str | None) -> None:
        if final_message:
            self.invoke(final_message)
        self.console.new_lines(1)

    def _get_default_profile(self) -> AgentProfile:
        return AGENT_PROFILES[self.role]

    def _create_executor(self, tools: list) -> AgentExecutor:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    self.profile,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )
        agent = create_openai_tools_agent(self._llm, tools, prompt)
        return AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
        )

    def create_planning_chain(self):
        system_prompt = f"""{self.profile}
Based on the user request provided, your task is to generate a detail and specific plan that includes following items:
    - action: it must be one of {", ".join(ACTIONS)}
    - working_directory: a directory where the command is to be executed or the file is to be placed, it should be started from '.', e.g. './src/'
    - filename: specify only if the name of the file to be added or changed is specifically determined
    - command: command to be executed if necessary
    - context: all contextual information that should be communicated to the person performing the task
    - objective: very detailed description of the objective to be achieved for the task to be executed to accomplish the entire plan
    - reason: clear reasons why the task should be performed

Make sure that each step has all the information needed - do not skip steps.
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
                                    "description": "Directory where the command is to be executed or the file is to be located, it should be started from '.', e.g. './src/'",
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
                                "objective": {
                                    "type": "string",
                                    "description": "Very detailed description of the goals to be achieved for the task to be executed to accomplish the entire plan",
                                },
                                "reason": {
                                    "type": "string",
                                    "reason": "Clear reasons why the task should be performed",
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

    def create_supervisor_chain(self, members: list = []):
        options = ["FINISH"] + members
        system_prompt = (
            "You are a supervisor tasked with managing a conversation between the"
            " following workers: {members}. Given the following user request,"
            " respond with the worker to act next. Each worker will perform a"
            " task and respond with their results and status. When finished,"
            " respond with FINISH."
        )
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
        ).partial(options=str(options), members=", ".join(members))

        return (
            prompt
            | self._llm.bind_functions(functions=[function_def], function_call="route")
            | JsonOutputFunctionsParser()
        )

    def create_git_commit_message_chain(self, members: list = []):
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

    def current_source_code(self) -> str:
        source_code_contents = []
        for (
            filename,
            file_content,
        ) in self.storages.app.recursive_file_search().items():
            if self.debug_mode:
                self.console.print(
                    f"Adding file {filename} to the prompt...", style="blue"
                )
            formatted_code = format_file_to_input(filename, file_content)
            source_code_contents.append(formatted_code)
        return "\n".join(source_code_contents)


def _create_llm(model_name: str, temperature: float) -> BaseChatModel:
    endpoint = os.getenv("ENDPOINT")
    if endpoint == "AZURE":
        return _create_azure_chat_openai_instance(
            os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        )
    else:
        return _create_chat_openai_instance(model_name, temperature)


def _create_chat_openai_instance(model_name: str, temperature: float):
    if model_name not in _get_supported_models():
        raise ValueError(f"Model {model_name} not supported")
    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        streaming=True,
        client=openai.chat.completions,
    )


def _create_azure_chat_openai_instance(model_name: str):
    return AzureChatOpenAI(
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-07-01-preview"),
        deployment_name=model_name,
        streaming=True,
    )


def _get_supported_models() -> list[str]:
    # cache the models list since it is unlikely to change frequently.
    @lru_cache(maxsize=1)
    def _fetch_supported_models():
        openai.api_type = "openai"
        return [model.id for model in openai.models.list()]

    return _fetch_supported_models()


class AgentRole(str, Enum):
    COPILOT = "copilot"
    PRODUCT_OWNER = "product_owner"
    ENGINEER = "engineer"
    ARCHITECT = "architect"
    DESIGNER = "designer"
    QA_ENGINEER = "qa_engineer"
    PROJECT_MANAGER = "project_manager"


@dataclass
class AgentProfile:
    name: str
    color: str
    prompt: PromptTemplate


AGENT_PROFILES = {
    AgentRole.COPILOT: AgentProfile(
        name="copilot",
        color="#C4C4C4",
        prompt=PromptTemplate.from_template(""),
    ),
    AgentRole.PRODUCT_OWNER: AgentProfile(
        name="Steve Jobs",
        color="#FBE7C6",
        prompt=PromptTemplate.from_template(
            """You are an experienced product owner who defines specification of a software application.
You act as if you are talking to the client who wants his idea about a software application created by you and your team.
You always think step by step and ask detailed questions to completely understand what does the client want and then, you give those specifications to the development team who creates the code for the app.
"""
        ),
    ),
    AgentRole.ENGINEER: AgentProfile(
        name="DHH",
        color="#B4F8C8",
        prompt=PromptTemplate.from_template(
            """You are a super engineer with excellent command of React, JavaScript, and chakra-ui.
Your job is to implement **fully working** applications.
Always follow the best practices for the requested languages and frameworks for folder/file structure and how to package the project.
"""
        ),
    ),
    AgentRole.ARCHITECT: AgentProfile(
        name="Jeff Dean",
        color="#A0E7E5",
        prompt=PromptTemplate.from_template(
            """You are a seasoned software architect, specializing in designing architectures for minimum viable products (MVPs) for web applications.
On the front-end side, you excel in React.js best practice.
"""
        ),
    ),
    AgentRole.DESIGNER: AgentProfile(
        name="Jonathan Ive",
        color="#FFAEBC",
        prompt=PromptTemplate.from_template(
            """You are an experienced designer at Apple, specializing in creating user-friendly interfaces and experiences that follow the Human Interface Guidelines.
Also skilled in understanding and using `chakra-ui` specifications.
Proactively use `react-icons`, and if you do, don't forget to include them in dependencies in package.json.
"""
        ),
    ),
    AgentRole.QA_ENGINEER: AgentProfile(
        name="Sam Altman",
        color="#65463E",
        prompt=PromptTemplate.from_template(
            """You are a super engineer who specializes in testing that an application is fully functional according to specifications.
You have an eye for detail and a knack for finding hidden bugs.
You check for import omissions, variable declarations, parenthesis mismatches, syntax errors, and more.
You also check for security vulnerabilities and logic errors.
"""
        ),
    ),
    AgentRole.PROJECT_MANAGER: AgentProfile(
        name="Elon Musk",
        color="#DCBAA9",
        prompt=PromptTemplate.from_template(
            """You are a world-class project manager with extensive knowledge of everything from coding to design and testing, managing projects with enthusiasm to bring applications to full completion.
"""
        ),
    ),
}
