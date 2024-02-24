from abc import ABC, abstractmethod

from gpt_all_star.core.agents.copilot import Copilot


class Step(ABC):
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        self.copilot = copilot
        self.copilot.console.section(f"STEP: {self.__class__.__name__}")
        self.working_directory = self.copilot.storages.root.path.absolute()
        self.exclude_dirs = [".archive", "node_modules", "build"]

    @abstractmethod
    def planning_prompt(self) -> str:
        pass

    @abstractmethod
    def additional_tasks(self) -> list:
        pass

    @abstractmethod
    def callback(self) -> None:
        pass
