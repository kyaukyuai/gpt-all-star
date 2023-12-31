from __future__ import annotations

from enum import Enum

import openai
from langchain_community.chat_models import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage

from core.Message import Message
from logger.logger import logger
from prompts.prompts import get_prompt


class Agent:
    def __init__(self, role: AgentRole) -> None:
        if not isinstance(role, str) or not role:
            raise ValueError("`role` should be a non-empty string")

        self.role: AgentRole = role
        self.print_role()

        self.llm = _create_llm('gpt-4', 0.1)
        self.messages: list[BaseMessage] = [
            Message.create_system_message(get_prompt(f"system_messages/{self.role.name}"))]

    def print_role(self) -> None:
        logger.info(f"The role of this agent is {self.role}")

    def chat(self, human_input: str | None) -> None:
        if human_input is not None:
            self.messages.append(Message.create_human_message(human_input))

        logger.info(f"Messages before chat: {self.messages}")

        callbacks = StreamingStdOutCallbackHandler()
        response = self.llm(self.messages, callbacks=[callbacks])
        self.messages.append(response)

        logger.info(f"Messages after chat: {self.messages}")

    def latest_message_content(self) -> str:
        return self.messages[-1].content.strip()

    def is_initialized(self) -> bool:
        return len(self.messages) <= 1


def _create_llm(model_name: str, temperature: float) -> BaseChatModel:
    supported_models = [model.id for model in openai.models.list()]

    if model_name not in supported_models:
        raise ValueError(f"Model {model_name} not supported")

    return ChatOpenAI(
        model=model_name,
        temperature=temperature,
        streaming=True,
        client=openai.chat.completions,
    )


class AgentRole(str, Enum):
    PRODUCT_OWNER = "product_owner"
    ENGINEER = "engineer"
