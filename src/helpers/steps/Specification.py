from langchain_core.messages import BaseMessage

from helpers import Agents
from helpers.Message import Message
from helpers.Step import Step
from helpers.Storage import Storages
from helpers.agents.ProductOwner import ProductOwner
from logger.logger import logger


class Specification(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> list[BaseMessage]:
        self.agents.product_owner.update_project_specification(None)
        self.agents.product_owner.chat(None)

        response = self.agents.product_owner.latest_message_content()
        logger.info(f"response: {response}")
        self.console.print()

        self.storages.result[self.__class__.__name__.lower()] = Message.serialize_messages(
            self.agents.product_owner.messages)
        file = Message.parse_message(self.agents.product_owner.latest_message_content())[0]
        self.storages.result['specification.md'] = file[1]
        return self.agents.product_owner.messages
