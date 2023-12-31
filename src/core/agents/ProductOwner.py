from __future__ import annotations

from langchain_core.messages import BaseMessage

from core.agents.Agent import Agent, AgentRole
from core.Message import Message
from prompts.prompts import get_prompt


class ProductOwner(Agent):
    def __init__(self) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER)

    def clarify_project(self, specification: str) -> None:
        prompt_message = Message.create_system_message(get_prompt('steps/clarify'))
        human_message = Message.create_human_message(specification)
        self.messages.extend([prompt_message, human_message])

    def create_specification(self, messages: list[BaseMessage] | None) -> None:
        if messages is not None:
            self.messages += messages

        self.messages.append(Message.create_system_message(get_prompt('steps/update_specification')))
