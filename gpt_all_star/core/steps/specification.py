from gpt_all_star.core.agents import agents
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

    def run(self) -> None:
        self.agents.product_owner.create_specifications(review_mode=self.review_mode)
        self.console.new_lines()
