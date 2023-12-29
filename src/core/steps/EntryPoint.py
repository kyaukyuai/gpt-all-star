from langchain_core.messages import BaseMessage

from core.Message import Message
from core.Storage import Storages
from core.agents.Agents import Agents
from core.steps.Step import Step
from logger.logger import logger


class EntryPoint(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> list[BaseMessage]:
        self.agents.engineer.generate_entrypoint()
        self.agents.engineer.chat(None)

        response = self.agents.engineer.latest_message_content()
        logger.info(f"response: {response}")
        self.console.print()

        self.storages.result[self.__class__.__name__.lower()] = Message.serialize_messages(
            self.agents.engineer.messages)

        return self.agents.engineer.messages
