from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
import os
from enum import Enum
from functools import lru_cache
import warnings
import openai
from langchain_community.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts.prompt import PromptTemplate
from rich.markdown import Markdown
from rich.panel import Panel

from gpt_all_star.cli.console_terminal import ConsoleTerminal
from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.logger.logger import logger

NEXT_COMMAND = "next"
warnings.simplefilter("ignore")


class Agent(ABC):
    def __init__(
        self,
        role: AgentRole,
        storages: Storages | None,
        name: str | None = None,
        profile: str | None = None,
        color: str | None = None,
    ) -> None:
        self._console = ConsoleTerminal()
        self._llm = _create_llm("gpt-4-32k", 0.1)

        self.role: AgentRole = role
        self.name: str = name or self._get_default_profile().name
        self.profile: str = profile or self._get_default_profile().prompt.format()
        self.color: str = color or self._get_default_profile().color

        self.messages: list[BaseMessage] = [Message.create_system_message(self.profile)]
        self.storages = storages

    def chat(self, human_input: str | None = None) -> None:
        if human_input is not None:
            self.messages.append(Message.create_human_message(human_input))

        logger.info(f"Messages before chat: {self.messages}")

        callbacks = StreamingStdOutCallbackHandler()
        response = self._llm(self.messages, callbacks=[callbacks])
        self.messages.append(response)

        logger.info(f"Messages after chat: {self.messages}")

    def state(self, text: str) -> None:
        self._console.print(f"{self.name}: {text}", style=f"bold {self.color}")

    def output_md(self, md: str) -> None:
        self._console.print(Panel(Markdown(md, style="bold")))

    def ask(self, question: str, is_required: bool = True, default: str = None) -> str:
        while True:
            default_value = f" (default: {default})" if default else ""
            self._console.print(
                f"[{self.color} bold]{self.name}: {question}[/{self.color} bold]{default_value}"
            )
            answer = self._console._input("project.history").strip() or default
            self._console.new_lines(1)

            logger.info("Question: %s", question)
            logger.info("Answer: %s", answer)

            if answer or not is_required:
                return answer
            print("No input provided! Please try again.")

    def present_choices(
        self,
        question: str,
        choices: list[str],
        default: str,
    ) -> str:
        return self._console._choice(
            f"{self.name}: {question} (default: {default})",
            choices=choices,
            default=default,
            style=f"bold {self.color}",
        )

    def latest_message_content(self) -> str:
        return self.messages[-1].content.strip()

    def _execute(
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

                self._console.new_lines(1)
                user_input = self.ask(follow_up_message)
                if user_input == NEXT_COMMAND:
                    self._handle_final_message(final_message)
                    break

            self.chat(user_input)
            self._console.new_lines(1)
            count += 1

    def _handle_final_message(self, final_message: str | None) -> None:
        if final_message:
            self.chat(final_message)
        self._console.new_lines(1)

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
        return [model.id for model in openai.models.list()]

    return _fetch_supported_models()


class AgentRole(str, Enum):
    COPILOT = "copilot"
    PRODUCT_OWNER = "product_owner"
    ENGINEER = "engineer"
    ARCHITECT = "architect"
    DESIGNER = "designer"


@dataclass
class AgentProfile:
    name: str
    color: str
    prompt: PromptTemplate


AGENT_PROFILES = {
    AgentRole.COPILOT: AgentProfile(
        name="copilot",
        color="#FBE7C6",
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
            """You are a full stack software developer working for a software development company.
You write very modular and clean code.
Your job is to implement **fully working** applications.

Almost always put different classes in different files.
Always use the programming language the user asks for.
For Python, you always create an appropriate requirements.txt file.
For NodeJS, you always create an appropriate package.json file.
Always add a comment briefly describing the purpose of the function definition.
Add comments explaining very complex bits of logic.
Always follow the best practices for the requested languages for folder/file structure and how to package the project.
"""
        ),
    ),
    AgentRole.ARCHITECT: AgentProfile(
        name="Jeff Dean",
        color="#FFAEBC",
        prompt=PromptTemplate.from_template(
            """You are a seasoned software architect, specializing in designing architectures for minimum viable products (MVPs) for web applications. Your approach emphasizes rapid development through the extensive use of pre-existing technologies.
"""
        ),
    ),
    AgentRole.DESIGNER: AgentProfile(
        name="Jonathan Ive",
        color="#E2F0CB",
        prompt=PromptTemplate.from_template(
            """You are an experienced designer. Your expertise is in creating user-friendly interfaces and experiences.
"""
        ),
    ),
}
