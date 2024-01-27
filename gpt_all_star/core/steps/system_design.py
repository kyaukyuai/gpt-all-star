from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class SystemDesign(Step):
    def __init__(self, agents: Agents, japanese_mode: bool, auto_mode: bool) -> None:
        super().__init__(agents, japanese_mode, auto_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the system design step!")
        self.console.new_lines()
        self.agents.architect.create_system_design(auto_mode=self.auto_mode)
        self.console.new_lines()
