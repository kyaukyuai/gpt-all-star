from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.entrypoint.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step


class Entrypoint(Step):
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        super().__init__(copilot)
        self.working_directory = self.copilot.storages.app.path.absolute()

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            current_source_code=self.copilot.storages.current_source_code(),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []

    def callback(self) -> None:
        self.copilot.output_files(exclude_dirs=[".archive", "node_modules"])
