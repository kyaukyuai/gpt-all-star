from langchain_core.messages import BaseMessage

from cli.prompt_toolkit import ask_user
from core.agents import Agents
from core.Message import Message
from core.steps.Step import Step, NEXT_COMMAND
from core.Storage import Storages
from logger.logger import logger


class Specification(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> list[BaseMessage]:
        message = Message.deserialize_messages(
            self.storages.memory['clarify']) if self.agents.product_owner.is_initialized() else None
        self.agents.product_owner.create_specification(message)

        user_input = None
        count = 0

        while True:
            if count > 0:
                self.console.print()
                user_input = ask_user(
                    f"Do you want to add any features or changes?"
                    f" If yes, describe it here and if no, just type `{NEXT_COMMAND}`"
                )
                if user_input == NEXT_COMMAND:
                    break

            self.agents.product_owner.chat(user_input)

            response = self.agents.product_owner.latest_message_content()
            logger.info(f"response: {response}")
            count += 1

        self.storages.memory[self.__class__.__name__.lower()] = Message.serialize_messages(
            self.agents.product_owner.messages)
        file = Message.parse_message(self.agents.product_owner.latest_message_content())[0]
        self.storages.memory['specification.md'] = file[1]
        return self.agents.product_owner.messages
