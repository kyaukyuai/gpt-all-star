from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.specification.additional_tasks import (
    create_additional_tasks,
)
from gpt_all_star.core.steps.step import Step


class Specification(Step):
    def __init__(
        self,
        copilot: Copilot,
    ) -> None:
        super().__init__(copilot)
        self.working_directory = self.copilot.storages.docs.path.absolute()

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        instructions = self.copilot.get_instructions()
        app_type = self.copilot.get_app_type()
        self.copilot.state("Ok, we have a instruction and app type now!")
        self.copilot.state(
            f"""
---
instruction:
{instructions}
app_type:
{app_type}
---
""",
        )
        return create_additional_tasks(app_type, instructions)

    def callback(self) -> None:
        self.copilot.output_md(self.copilot.storages.docs.get("specifications.md", ""))
