from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import additional_tasks


class SystemDesign(Step):
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        super().__init__(copilot)
        self.working_directory = self.copilot.storages.docs.path.absolute()

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        return additional_tasks

    def callback(self) -> bool:
        technologies = self.copilot.storages.docs.get("technologies.md")
        has_technologies = bool(technologies)
        if has_technologies:
            self.copilot.output_md(technologies)
        return has_technologies
