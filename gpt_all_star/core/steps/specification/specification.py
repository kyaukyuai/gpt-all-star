from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.specification.additional_tasks import (
    create_additional_tasks,
)
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.storage import Storages


class Specification(Step):
    def __init__(
        self,
        copilot: Copilot,
        storages: Storages,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(copilot, storages, japanese_mode, review_mode, debug_mode)

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        instructions = self.copilot.get_instructions()
        app_type = self.copilot.get_app_type()
        self.copilot.state("Ok, we have a instruction and app type now!")
        self.copilot.console.print(
            f"""
---
instruction:
{instructions}
app_type:
{app_type}
---
""",
            style="bold",
        )
        return create_additional_tasks(app_type, instructions)
