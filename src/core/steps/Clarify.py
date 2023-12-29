from langchain_core.messages import BaseMessage

from core.agents.Agents import Agents
from core.Message import Message
from core.steps.Step import Step, NEXT_COMMAND
from core.Storage import Storages
from logger.logger import logger
from cli.prompt_toolkit import get_input


class Clarify(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> list[BaseMessage]:
        self.agents.product_owner.get_project_description(self.storages.origin['specification.md'])

        user_input = None
        response = ""
        count = 0

        while "nothing to clarify" not in response.lower():
            if count > 0:
                user_input = get_input('project.history', set())
                if user_input == NEXT_COMMAND:
                    self.agents.product_owner.chat(
                        "Make your own assumptions and state them explicitly, and please answer 'Clear'")
                    self.console.print()
                    break

            self.agents.product_owner.chat(user_input)

            response = self.agents.product_owner.latest_message_content()
            logger.info(f"response: {response}")

            count += 1
            self.console.print()
            self.console.print(f"Answer in text, or o proceed to the next step, type `{NEXT_COMMAND}`",
                               style='bold yellow')
            self.console.print()

        self.storages.result[self.__class__.__name__.lower()] = Message.serialize_messages(
            self.agents.product_owner.messages)
        return self.agents.product_owner.messages
