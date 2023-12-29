from langchain_core.messages import BaseMessage

from core.Message import Message
from core.agents.Agent import Agent, AgentRole
from prompts.prompts import get_prompt


class Engineer(Agent):
    def __init__(self) -> None:
        super().__init__(AgentRole.ENGINEER)

    def develop(self, specification: str):
        self.messages.append(Message.create_system_message(get_prompt('steps/development')))
        self.messages.append(Message.create_human_message(specification))
