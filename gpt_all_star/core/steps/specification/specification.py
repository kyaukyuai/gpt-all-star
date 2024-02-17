from gpt_all_star.core.agents import agents
from gpt_all_star.core.steps.specification.additional_tasks import (
    create_additional_tasks,
)
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class Specification(Step):
    def __init__(
        self,
        agents: agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        instructions = self.agents.product_owner.get_instructions()
        app_type = self.agents.product_owner.get_app_type()

        team = Team(supervisor=self.agents.product_owner, members=self.agents.members())

        team.drive(None, create_additional_tasks(app_type, instructions))
