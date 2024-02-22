from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.improvement.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.storage import Storages


class Improvement(Step):
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
        request = self.copilot.ask(
            "What would you like to update?", is_required=True, default=None
        )

        planning_prompt = planning_prompt_template.format(
            request=request,
            current_source_code=self.storages.current_source_code(),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []
