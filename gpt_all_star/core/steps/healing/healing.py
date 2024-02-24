from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.healing.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step


class Healing(Step):
    def __init__(self, copilot: Copilot, error_message: str) -> None:
        super().__init__(copilot)
        self.error_message = error_message
        self.working_directory = self.copilot.storages.app.path.absolute()

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            error=self.error_message,
            current_source_code=self.copilot.storages.current_source_code(),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []

    def callback(self) -> None:
        self.copilot.output_files(exclude_dirs=self.exclude_dirs)
