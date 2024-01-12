from __future__ import annotations
from abc import ABC

import os
from enum import Enum
from functools import lru_cache
import warnings

import openai
from langchain_community.chat_models import AzureChatOpenAI, ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from rich.markdown import Markdown
from rich.panel import Panel

from your_dev_team.cli.ConsoleTerminal import ConsoleTerminal
from your_dev_team.core.Message import Message
from your_dev_team.core.Storage import Storages
from your_dev_team.logger.logger import logger

NEXT_COMMAND = "next"
warnings.simplefilter("ignore")


class Agent(ABC):
    def __init__(
        self, role: AgentRole, storages: Storages, name: str = "", profile: str = ""
    ) -> None:
        self._console = ConsoleTerminal()
        self._llm = _create_llm("gpt-4", 0.1)

        self.role: AgentRole = role
        self.name: str = name
        self.profile: str = profile

        self.messages: list[BaseMessage] = [Message.create_system_message(self.profile)]
        self.storages = storages

    def chat(self, human_input: str | None) -> None:
        if human_input is not None:
            self.messages.append(Message.create_human_message(human_input))

        logger.info(f"Messages before chat: {self.messages}")

        callbacks = StreamingStdOutCallbackHandler()
        response = self._llm(self.messages, callbacks=[callbacks])
        self.messages.append(response)

        logger.info(f"Messages after chat: {self.messages}")

    def state(self, text: str) -> None:
        self._console.print(
            f"{self.name}: {text}", style=f"bold {AgentRole.color_scheme()[self.role]}"
        )

    def output_md(self, md: str) -> None:
        self._console.print(Panel(Markdown(md, style="bold")))

    def ask(
        self, question: str, require_answer: bool = True, default_value: str = None
    ) -> str:
        while True:
            default = f" (default: {default_value})" if not require_answer else ""
            self._console.print(
                f"[{AgentRole.color_scheme()[self.role]} bold]{self.name}: {question}[/{AgentRole.color_scheme()[self.role]} bold]{default}"
            )
            answer = self._console._input("project.history").strip() or default_value
            self._console.new_lines(1)

            logger.info("Question: %s", question)
            logger.info("Answer: %s", answer)

            if not answer:
                if require_answer:
                    print("No input provided! Please try again.")
                else:
                    print("Exiting application.")
                    exit(0)
            else:
                return answer

    def latest_message_content(self) -> str:
        return self.messages[-1].content.strip()

    def is_initialized(self) -> bool:
        return len(self.messages) <= 1

    def _execute(
        self, follow_up_message: str, final_message: str | None = None
    ) -> None:
        user_input = None
        count = 0

        while True:
            if count > 0:
                self._console.new_lines(2)
                user_input = self.ask(follow_up_message)
                if user_input == NEXT_COMMAND:
                    if final_message:
                        self.chat(final_message)
                        self._console.new_lines(1)
                    self._console.new_lines(1)
                    break

            self.chat(user_input)
            count += 1


def _create_llm(model_name: str, temperature: float) -> BaseChatModel:
    endpoint = os.getenv("ENDPOINT")
    if endpoint == "AZURE":
        return _create_azure_chat_openai_instance(model_name)
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
        openai_api_version=os.getenv("OPENAI_API_VERSION", "2023-05-15"),
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

    @classmethod
    def default_name(cls):
        return {
            cls.COPILOT: "copilot",
            cls.PRODUCT_OWNER: "Steve Jobs",
            cls.ENGINEER: "DHH",
            cls.ARCHITECT: "Jeff Dean",
        }

    @classmethod
    def color_scheme(cls):
        # Pastel Dreams color combination from https://www.canva.com/colors/color-palettes/pastel-dreams/
        return {
            cls.COPILOT: "#FBE7C6",
            cls.PRODUCT_OWNER: "#B4F8C8",
            cls.ENGINEER: "#A0E7E5",
            cls.ARCHITECT: "#FFAEBC",
        }
