from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.additional_tasks import create_additional_tasks
from gpt_all_star.core.steps.ui_design.improvement_prompt import (
    improvement_prompt_template,
)


class UIDesign(Step):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display, japanese_mode)
        self.working_directory = self.copilot.storages.docs.path.absolute()

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        return create_additional_tasks()

    def callback(self) -> bool:
        ui_design = self.copilot.storages.docs.get("ui_design.html")
        has_ui_design = bool(ui_design)
        if has_ui_design:
            self.copilot.output_html(ui_design)
        return has_ui_design

    def improvement_prompt(self) -> str:
        request = self.improvement_request or self.copilot.ask(
            self._("What do you want to update?"), is_required=True, default=None
        )
        improvement_prompt = improvement_prompt_template.format(
            request=request,
            ui_design=self.copilot.storages.docs.get("ui_design.html", "N/A"),
        )
        return improvement_prompt
