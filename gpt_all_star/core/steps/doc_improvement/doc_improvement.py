from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.doc_improvement.planning_prompt import (
    planning_prompt_template,
)
from gpt_all_star.core.steps.step import Step


class DocImprovement(Step):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display, japanese_mode)
        self.working_directory = self.copilot.storages.docs.path.absolute()
        self.request = ""

    def planning_prompt(self) -> str:
        request = self.request or self.copilot.ask(
            self._("What would you like to update?"), is_required=True, default=None
        )
        planning_prompt = planning_prompt_template.format(
            request=request,
            specifications=self.copilot.storages.docs.get("specifications.md", "N/A"),
            technologies=self.copilot.storages.docs.get("technologies.md", "N/A"),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []

    def callback(self) -> bool:
        return True
