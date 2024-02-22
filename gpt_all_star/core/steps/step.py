from abc import ABC, abstractmethod

from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.storage import Storages


class Step(ABC):
    def __init__(
        self,
        copilot: Copilot,
        storages: Storages,
    ) -> None:
        self.copilot = copilot
        self.storages = storages

        self.copilot.console.section(f"STEP: {self.__class__.__name__}")

    @abstractmethod
    def planning_prompt(self) -> str:
        pass

    @abstractmethod
    def additional_tasks(self) -> list:
        pass
