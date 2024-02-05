from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class SystemDesign(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        self.agents.architect.create_system_design(review_mode=self.review_mode)
        self.console.new_lines()
