from abc import ABC, abstractmethod

from gpt_all_star.cli.console_terminal import ConsoleTerminal
from gpt_all_star.core.agents.agents import Agents


class Step(ABC):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool = False,
        review_mode: bool = False,
        debug_mode: bool = False,
    ) -> None:
        self.agents = agents
        self.japanese_mode = japanese_mode
        self.review_mode = review_mode
        self.debug_mode = debug_mode
        self.console = ConsoleTerminal()

        self.console.section(f"STEP: {self.__class__.__name__}")

    @abstractmethod
    def planning_prompt(self) -> str:
        pass

    @abstractmethod
    def additional_tasks(self) -> list:
        pass
