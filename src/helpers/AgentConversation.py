from __future__ import annotations

import json

import openai
from langchain_community.chat_models import ChatOpenAI
from langchain_core.callbacks import StreamingStdOutCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage, messages_to_dict, \
    messages_from_dict
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

    @staticmethod
    def serialize_messages(messages: list[BaseMessage]) -> str:
        return json.dumps(messages_to_dict(messages))

    @staticmethod
    def deserialize_messages(json_dict_str: str) -> list[BaseMessage]:
        data = json.loads(json_dict_str)
        pre_validated_data = [{
            **item, "data": {
                **item["data"], "is_chunk": False
            }
        } for item in data]
        return list(messages_from_dict(pre_validated_data))

    def next(self, messages: list[BaseMessage], prompt: str | None) -> list[BaseMessage]:
        if prompt is not None:
            self.messages.append(AgentConversation.create_human_message(prompt))

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
