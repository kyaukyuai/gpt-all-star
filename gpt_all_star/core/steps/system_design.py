from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class SystemDesign(Step):
    def __init__(self, agents: Agents, japanese_mode) -> None:
        super().__init__(agents, japanese_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the system design step!")
        self.console.new_lines(1)
        self.agents.architect.state("How about the following?")
        self.agents.architect.list_technology_stack()
        self.console.new_lines(1)
        self.agents.architect.state("How about the following?")
        self.agents.architect.layout_directory()
        self.console.new_lines(1)
