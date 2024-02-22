from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import additional_tasks
from gpt_all_star.core.storage import Storages


class SystemDesign(Step):
    def __init__(
        self,
        copilot: Copilot,
        storages: Storages,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(copilot, storages, japanese_mode, review_mode, debug_mode)

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        return additional_tasks
