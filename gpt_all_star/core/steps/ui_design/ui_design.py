from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.planning_prompt import planning_prompt_template
from gpt_all_star.core.storage import Storages


class UIDesign(Step):
    def __init__(
        self,
        copilot: Copilot,
        storages: Storages,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(copilot, storages, review_mode, debug_mode)

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            current_source_code=self.storages.current_source_code(),
            specifications=self.storages.docs.get("specifications.md", "N/A"),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []
