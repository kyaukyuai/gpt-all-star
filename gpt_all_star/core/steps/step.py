from abc import ABC, abstractmethod

from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.helper.translator import create_translator


class Step(ABC):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        self.copilot = copilot
        self.working_directory = self.copilot.storages.root.path.absolute()
        self.plan_and_solve = False
        self.exclude_dirs = [".archive", "node_modules", "build"]
        self.display = display
        self.improvement_request = None

        if self.display:
            self.copilot.console.section(f"STEP: {self.__class__.__name__}")

        self._ = create_translator("ja" if japanese_mode else "en")

    @abstractmethod
    def planning_prompt(self) -> str:
        pass

    @abstractmethod
    def additional_tasks(self) -> list:
        pass

    @abstractmethod
    def callback(self) -> bool:
        pass

    @abstractmethod
    def improvement_prompt(self) -> str:
        pass
