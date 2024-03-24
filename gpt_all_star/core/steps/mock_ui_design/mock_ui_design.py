from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.mock_ui_design.additional_tasks import additional_tasks
from gpt_all_star.core.steps.step import Step


class MockUiDesign(Step):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display, japanese_mode)
        self.working_directory = self.copilot.storages.docs.path.absolute()

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        return additional_tasks

    def callback(self) -> bool:
        design_html = self.copilot.storages.docs.get("design_000.html")
        has_design = bool(design_html)
        if has_design:
            self.copilot.output_files(design_html)

        return has_design
