from abc import ABC, abstractmethod

from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.storage import Storages


class Step(ABC):
    def __init__(
        self,
        copilot: Copilot,
        storages: Storages,
        japanese_mode: bool = False,
        review_mode: bool = False,
        debug_mode: bool = False,
    ) -> None:
        self.copilot = copilot
        self.storages = storages
        self.japanese_mode = japanese_mode
        self.review_mode = review_mode
        self.debug_mode = debug_mode

        self.copilot.console.section(f"STEP: {self.__class__.__name__}")

    @abstractmethod
    def planning_prompt(self) -> str:
        pass

    @abstractmethod
    def additional_tasks(self) -> list:
        pass
