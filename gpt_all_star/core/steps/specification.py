from gpt_all_star.core.agents import agents
from gpt_all_star.core.steps.step import Step


class Specification(Step):
    def __init__(self, agents: agents, japanese_mode) -> None:
        super().__init__(agents, japanese_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the specification step!")
        self.console.new_lines()
        self.agents.product_owner.clarify_instructions()
        self.agents.product_owner.state("How about the following?")
        self.agents.product_owner.summarize_specifications()
        self.console.new_lines()
