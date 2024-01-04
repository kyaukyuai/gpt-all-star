from core.agents.Agents import Agents
from core.Message import Message
from core.steps.Step import Step, NEXT_COMMAND
from core.Storage import Storages


class Clarify(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        messages = self.agents.product_owner.clarify_specification(self._get_instructions())
        self.storages.memory[self.__class__.__name__.lower()] = Message.serialize_messages(messages)

    def _get_instructions(self) -> str:
        return (
            self.storages.origin['instructions']
            if self.storages.origin.get('instructions') is not None
            else self.terminal.ask_user("What application do you want to generate?")
        )
