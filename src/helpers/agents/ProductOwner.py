from __future__ import annotations

from langchain_core.messages import BaseMessage

from helpers.Agent import Agent, AgentRole
from helpers.Message import Message
from utils.prompts import get_prompt


class ProductOwner(Agent):
    def __init__(self) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER)

    def get_project_description(self, specification: str):
        self.messages.append(Message.create_system_message(get_prompt('steps/clarify')))
        self.messages.append(Message.create_human_message(specification))

    def update_project_specification(self, messages: list[BaseMessage] | None) -> None:
        if messages is not None:
            self.messages += messages

        self.messages.append(Message.create_system_message(get_prompt('steps/update_specification')))
