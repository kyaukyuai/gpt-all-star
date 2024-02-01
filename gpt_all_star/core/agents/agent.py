from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
import os
from enum import Enum
from functools import lru_cache
import re
import openai
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts.prompt import PromptTemplate
from rich.markdown import Markdown
from rich.panel import Panel

from gpt_all_star.cli.console_terminal import ConsoleTerminal
from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.tool.text_parser import TextParser

NEXT_COMMAND = "next"


class Agent(ABC):
    def __init__(
        self,
        role: AgentRole,
        storages: Storages | None,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
        color: str | None = None,
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

    def chat(self, human_input: str | None = None) -> None:
        if human_input is not None:
            self.messages.append(Message.create_human_message(human_input))

        callbacks = [StreamingStdOutCallbackHandler()] if self.debug_mode else []
        response = self._llm(self.messages, callbacks=callbacks)
        self.messages.append(response)

    def state(self, text: str) -> None:
        self.console.print(f"{self.name}: {text}", style=f"bold {self.color}")

    def store_md(self, file_name_prefix: str, message: str) -> None:
        file = TextParser.parse_code_from_text(message)[0]
        self.storages.docs[f"{file_name_prefix}.md"] = file[1]

        self.state(f"These are the {file_name_prefix} used to build the application:")
        self._output_md(self.storages.docs[f"{file_name_prefix}.md"])

    def _output_md(self, md: str) -> None:
        self.console.print(Panel(Markdown(md, style="bold")))

    def ask(self, question: str, is_required: bool = True, default: str = None) -> str:
        while True:
            if default and default.endswith("\n"):
                default = re.sub(r"\n$", "", default)
            default_value = f"\n(default: {default})" if default else ""
            self.console.print(
                f"[{self.color} bold]{self.name}: {question}[/{self.color} bold][black]{default_value}[/black]"
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
        auto_mode: bool = False,
    ) -> None:
        user_input = None
        count = 0

        while True:
            if count > 0:
                if auto_mode:
                    self._handle_final_message(final_message)
                    break

                self.console.new_lines(1)
                user_input = self.ask(follow_up_message)
                if user_input == NEXT_COMMAND:
                    self._handle_final_message(final_message)
                    break

            self.chat(user_input)
            self.console.new_lines(1)
            count += 1

    def _handle_final_message(self, final_message: str | None) -> None:
        if final_message:
            self.chat(final_message)
        self.console.new_lines(1)

    def _get_default_profile(self) -> AgentProfile:
        return AGENT_PROFILES[self.role]


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
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
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


@dataclass
class AgentProfile:
    name: str
    color: str
    prompt: PromptTemplate


AGENT_PROFILES = {
    AgentRole.COPILOT: AgentProfile(
        name="copilot",
        color="#9D86E9",
        prompt=PromptTemplate.from_template(""),
    ),
    AgentRole.PRODUCT_OWNER: AgentProfile(
        name="Steve Jobs",
        color="#B4F8C8",
        prompt=PromptTemplate.from_template(
            """You are an experienced product owner who defines specification of a software application.
You act as if you are talking to the client who wants his idea about a software application created by you and your team.
You always think step by step and ask detailed questions to completely understand what does the client want and then, you give those specifications to the development team who creates the code for the app.
"""
        ),
    ),
    AgentRole.ENGINEER: AgentProfile(
        name="DHH",
        color="#A0E7E5",
        prompt=PromptTemplate.from_template(
            """You are a super engineer with excellent command of React, JavaScript, and chakra-ui.
Your job is to implement **fully working** applications.

Always follow the best practices for the requested languages and frameworks for folder/file structure and how to package the project.
For NodeJS, you always create an appropriate package.json file.
    - please set NODE_OPTIONS=--openssl-legacy-provider like so:
        "start": "NODE_OPTIONS=--openssl-legacy-provider react-scripts start"
        "build": "NODE_OPTIONS=--openssl-legacy-provider react-scripts build"
    - Do not include the homepage item in package.json.
"""
        ),
    ),
    AgentRole.ARCHITECT: AgentProfile(
        name="Jeff Dean",
        color="#FFAEBC",
        prompt=PromptTemplate.from_template(
            """You are a seasoned software architect, specializing in designing architectures for minimum viable products (MVPs) for web applications.
On the front-end side, you excel in React.js design.
"""
        ),
    ),
    AgentRole.DESIGNER: AgentProfile(
        name="Jonathan Ive",
        color="#E2F0CB",
        prompt=PromptTemplate.from_template(
            """You are an experienced designer at Apple, specializing in creating user-friendly interfaces and experiences that follow the Human Interface Guidelines.
Also skilled in understanding and using `chakra-ui` specifications.
Proactively use `react-icons`, and if you do, don't forget to include them in dependencies in package.json.
"""
        ),
    ),
    AgentRole.QA_ENGINEER: AgentProfile(
        name="Elon Musk",
        color="#FFB001",
        prompt=PromptTemplate.from_template(
            """You are a super engineer who specializes in testing that an application is fully functional according to specifications.
You have an eye for detail and a knack for finding hidden bugs.
You check for import omissions, variable declarations, parenthesis mismatches, syntax errors, and more.
You also check for security vulnerabilities and logic errors.
"""
        ),
    ),
}
