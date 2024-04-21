from abc import ABC, abstractmethod

from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.implementation_prompt import implementation_prompt_template
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
    def assign_prompt(self) -> str:
        pass

    @abstractmethod
    def planning_prompt(self) -> str:
        pass

    @abstractmethod
    def additional_tasks(self) -> list:
        pass

    def implementation_prompt(self, task: str, context: str) -> str:
        return implementation_prompt_template.format(
            task=task,
            context=context,
            implementation=self.copilot.storages.current_source_code(
                debug_mode=self.copilot.debug_mode
            ),
            specifications=self.copilot.storages.docs.get("specifications.md", "N/A"),
            technologies=self.copilot.storages.docs.get("technologies.md", "N/A"),
            ui_design=self.copilot.storages.docs.get("ui_design.html", "N/A"),
        )

    @abstractmethod
    def callback(self) -> bool:
        pass

    @abstractmethod
    def improvement_prompt(self) -> str:
        pass
