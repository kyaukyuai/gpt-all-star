from gpt_all_star.core.agents import agents
from gpt_all_star.core.steps.specification.additional_tasks import (
    create_additional_tasks,
)
from gpt_all_star.core.steps.step import Step


class Specification(Step):
    def __init__(
        self,
        agents: agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        instructions = self.agents.product_owner.get_instructions()
        app_type = self.agents.product_owner.get_app_type()
        self.agents.copilot.state("Ok, we have a instruction and app type now!")
        self.agents.copilot.console.print(
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
