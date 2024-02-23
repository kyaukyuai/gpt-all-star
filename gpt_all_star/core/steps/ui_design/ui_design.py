from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.planning_prompt import planning_prompt_template


class UIDesign(Step):
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        super().__init__(copilot)

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            current_source_code=self.copilot.storages.current_source_code(),
            specifications=self.copilot.storages.docs.get("specifications.md", "N/A"),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []

    def callback(self) -> None:
        self.copilot.output_files(exclude_dirs=[".archive", "node_modules"])
