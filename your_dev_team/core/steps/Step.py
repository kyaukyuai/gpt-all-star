from abc import ABC, abstractmethod

from langchain_core.messages import BaseMessage

from your_dev_team.cli.ConsoleTerminal import ConsoleTerminal
from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.Storage import Storages


class Step(ABC):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        self.agents = agents
        self.storages = storages
        self.console = ConsoleTerminal()

        self.console.section(f"STEP: {self.__class__.__name__}")

    @abstractmethod
    def run(self) -> list[BaseMessage]:
        pass
