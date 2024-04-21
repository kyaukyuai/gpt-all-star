from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.specification.additional_tasks import (
    create_additional_tasks,
)
from gpt_all_star.core.steps.specification.implementation_prompt import (
    implementation_prompt_template,
)
from gpt_all_star.core.steps.specification.improvement_prompt import (
    improvement_prompt_template,
)
from gpt_all_star.core.steps.step import Step


class Specification(Step):
    def __init__(
        self, copilot: Copilot, display: bool = True, japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display, japanese_mode)
        self.working_directory = self.copilot.storages.docs.path.absolute()
        self.instructions = ""
        self.app_type = ""

    def assign_prompt(self) -> str:
        return "We want to generate concise specifications for the web application."

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        instructions = (
            self.copilot.get_instructions()
            if self.instructions == ""
            else self.instructions
        )
        app_type = self.copilot.get_app_type() if self.app_type == "" else self.app_type
        if self.display:
            self.copilot.state(
                self._(
                    """
Ok, we have a instruction and app type now!
---
instruction:
%s
app_type:
%s
---
""",
                )
                % (instructions, app_type)
            )
        return create_additional_tasks(app_type, instructions)

    def implementation_prompt(self, task: str, context: str) -> str:
        return implementation_prompt_template.format(
            task=task,
            context=context,
        )

    def callback(self) -> bool:
        specifications = self.copilot.storages.docs.get("specifications.md")
        has_specifications = bool(specifications)
        if has_specifications:
            self.copilot.output_md(specifications)
        return has_specifications

    def improvement_prompt(self) -> str:
        request = self.improvement_request or self.copilot.ask(
            self._("What do you want to update?"), is_required=True, default=None
        )
        improvement_prompt = improvement_prompt_template.format(
            request=request,
            specifications=self.copilot.storages.docs.get("specifications.md", "N/A"),
        )
        return improvement_prompt
