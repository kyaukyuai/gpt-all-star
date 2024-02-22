from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.development.additional_tasks import additional_tasks
from gpt_all_star.core.steps.development.nodejs_tasks import nodejs_tasks
from gpt_all_star.core.steps.development.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.storage import Storages


class Development(Step):
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
        planning_prompt = planning_prompt_template.format(
            specifications=self.storages.docs.get("specifications.md", "N/A"),
            technologies=self.storages.docs.get("technologies.md", "N/A"),
            files=self.storages.docs.get("files.md", "N/A"),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return additional_tasks + nodejs_tasks
