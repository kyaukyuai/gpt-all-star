from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.entrypoint.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step


class Entrypoint(Step):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display, japanese_mode)
        self.working_directory = self.copilot.storages.app.path.absolute()

    def assign_prompt(self) -> str:
        assign_prompt = planning_prompt_template.format(
            current_source_code=self.copilot.storages.current_source_code(
                debug_mode=self.copilot.debug_mode
            ),
        )
        return assign_prompt

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            current_source_code=self.copilot.storages.current_source_code(
                debug_mode=self.copilot.debug_mode
            ),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []

    def callback(self) -> bool:
        self.copilot.output_files(exclude_dirs=self.exclude_dirs)
        return True

    def improvement_prompt(self) -> str:
        return ""
