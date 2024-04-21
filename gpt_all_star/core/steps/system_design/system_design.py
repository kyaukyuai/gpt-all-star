from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import (
    create_additional_tasks,
)
from gpt_all_star.core.steps.system_design.implementation_prompt import (
    implementation_prompt_template,
)
from gpt_all_star.core.steps.system_design.improvement_prompt import (
    improvement_prompt_template,
)


class SystemDesign(Step):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display, japanese_mode)
        self.working_directory = self.copilot.storages.docs.path.absolute()

    def assign_prompt(self) -> str:
        return "We want to generate concise system design."

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        return create_additional_tasks()

    def implementation_prompt(self, task: str, context: str) -> str:
        return implementation_prompt_template.format(
            task=task,
            context=context,
            specifications=self.copilot.storages.docs.get("specifications.md", "N/A"),
        )

    def callback(self) -> bool:
        technologies = self.copilot.storages.docs.get("technologies.md")
        has_technologies = bool(technologies)
        if has_technologies:
            self.copilot.output_md(technologies)
        return has_technologies

    def improvement_prompt(self) -> str:
        request = self.improvement_request or self.copilot.ask(
            self._("What do you want to update?"), is_required=True, default=None
        )
        improvement_prompt = improvement_prompt_template.format(
            request=request,
            technologies=self.copilot.storages.docs.get("technologies.md", "N/A"),
        )
        return improvement_prompt
