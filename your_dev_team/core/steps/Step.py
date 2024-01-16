from abc import ABC, abstractmethod
import warnings

from your_dev_team.cli.ConsoleTerminal import ConsoleTerminal
from your_dev_team.core.agents.Agents import Agents

warnings.simplefilter("ignore")


class Step(ABC):
    def __init__(self, agents: Agents, japanese_mode: bool = False) -> None:
        self.agents = agents
        self.japanese_mode = japanese_mode
        self.console = ConsoleTerminal()

        self.console.section(f"STEP: {self.__class__.__name__}")

    @abstractmethod
    def run(self) -> None:
        pass
