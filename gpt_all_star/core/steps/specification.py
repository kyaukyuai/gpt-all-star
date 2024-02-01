from gpt_all_star.core.agents import agents
from gpt_all_star.core.steps.step import Step


class Specification(Step):
    def __init__(
        self, agents: agents, japanese_mode: bool, auto_mode: bool, debug_mode: bool
    ) -> None:
        super().__init__(agents, japanese_mode, auto_mode, debug_mode)

    def run(self) -> None:
        self.agents.product_owner.create_specifications(auto_mode=self.auto_mode)
        self.console.new_lines()
