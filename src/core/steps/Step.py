from abc import ABC, abstractmethod

from langchain_core.messages import BaseMessage

from cli.Terminal import ConsoleTerminal
from core.agents.Agents import Agents
from core.Storage import Storages


class Step(ABC):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        self.agents = agents
        self.storages = storages
        self.terminal = ConsoleTerminal()

        self.terminal.section(f"STEP: {self.__class__.__name__}")

    @abstractmethod
    def run(self) -> list[BaseMessage]:
        pass
