from __future__ import annotations

import openai
from langchain_community.chat_models import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from openai import OpenAI
import tiktoken

from logger.logger import logger
from utils.prompts import get_prompt


class AgentConversation:
    def __init__(self, agent):
        self.llm = create_llm('gpt-4', 0.1)
        self.messages: list[BaseMessage] = []
        self.agent = agent
        self.high_level_step = self.agent.project.current_step

        self.messages.append(
            AgentConversation.create_system_message(
                get_prompt(f"system_messages/{agent.role}")))

    @staticmethod
    def create_system_message(message: str) -> SystemMessage:
        return SystemMessage(content=message)

    @staticmethod
    def create_human_message(message: str) -> HumanMessage:
        return HumanMessage(content=message)

    @staticmethod
    def create_ai_message(message: str) -> AIMessage:
        return AIMessage(content=message)

    def next(self, messages: list[BaseMessage], prompt: str | None) -> list[BaseMessage]:
        if prompt is not None:
            self.messages.append(AgentConversation.create_system_message(prompt))

        logger.info(f"Creating a new chat completion: {messages}")

        callbacks = StreamingStdOutCallbackHandler()
        response = self.llm(messages, callbacks=[callbacks])

        messages.append(response)
        logger.info(f"Received response: {response}")

        return messages


def create_llm(model: str, temperature: float) -> BaseChatModel:
    supported_models = [model.id for model in openai.models.list()]

    if model not in supported_models:
        raise ValueError(f"Model {model} not supported")

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        streaming=True,
        client=openai.chat.completions,
    )
