from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import additional_tasks


class SystemDesign(Step):
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        super().__init__(copilot)

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        return additional_tasks

    def callback(self) -> None:
        self.copilot.output_md(self.copilot.storages.docs.get("technologies.md", ""))
        self.copilot.output_md(self.copilot.storages.docs.get("files.md", ""))
