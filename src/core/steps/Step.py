from abc import ABC, abstractmethod

from langchain_core.messages import BaseMessage
from rich.console import Console

from core.agents.Agents import Agents
from core.Storage import Storages

NEXT_COMMAND = "next"


class Step(ABC):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        self.agents = agents
        self.storages = storages
        self.console = Console()

        self.console.rule(f"STEP: {self.__class__.__name__}")

    @abstractmethod
    def run(self) -> list[BaseMessage]:
        pass
