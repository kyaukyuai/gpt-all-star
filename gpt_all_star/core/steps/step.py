from abc import ABC, abstractmethod
import warnings

from gpt_all_star.cli.console_terminal import ConsoleTerminal
from gpt_all_star.core.agents.agents import Agents

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
