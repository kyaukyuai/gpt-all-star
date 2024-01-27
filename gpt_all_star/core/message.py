from __future__ import annotations

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)


class Message:
    @staticmethod
    def create_system_message(message: str) -> SystemMessage:
        return SystemMessage(content=message)

    @staticmethod
    def create_human_message(message: str) -> HumanMessage:
        return HumanMessage(content=message)

    @staticmethod
    def create_ai_message(message: str) -> AIMessage:
        return AIMessage(content=message)
