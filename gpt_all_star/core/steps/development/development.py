from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.development.additional_tasks import additional_tasks
from gpt_all_star.core.steps.development.nodejs_tasks import nodejs_tasks
from gpt_all_star.core.steps.development.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step


class Development(Step):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display, japanese_mode)
        self.working_directory = self.copilot.storages.app.path.absolute()
        self.plan_and_solve = True

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            specifications=self.copilot.storages.docs.get("specifications.md", "N/A"),
            technologies=self.copilot.storages.docs.get("technologies.md", "N/A"),
            system_architecture=self.copilot.storages.docs.get(
                "system_architecture.md", "N/A"
            ),
            design_html=self.copilot.storages.docs.get("design_000.html", "N/A"),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return additional_tasks + nodejs_tasks

    def callback(self) -> bool:
        self.copilot.output_files(exclude_dirs=self.exclude_dirs)
        return True
