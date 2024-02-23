from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.development.additional_tasks import additional_tasks
from gpt_all_star.core.steps.development.nodejs_tasks import nodejs_tasks
from gpt_all_star.core.steps.development.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step


class Development(Step):
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        super().__init__(copilot)
        self.working_directory = self.copilot.storages.app.path.absolute()

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            specifications=self.copilot.storages.docs.get("specifications.md", "N/A"),
            technologies=self.copilot.storages.docs.get("technologies.md", "N/A"),
            files=self.copilot.storages.docs.get("files.md", "N/A"),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return additional_tasks + nodejs_tasks

    def callback(self) -> None:
        self.copilot.output_files(exclude_dirs=[".archive", "node_modules"])
