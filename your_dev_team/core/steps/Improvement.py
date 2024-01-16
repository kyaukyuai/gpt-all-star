from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.steps.Step import Step


class Improvement(Step):
    def __init__(self, agents: Agents, japanese_mode) -> None:
        super().__init__(agents, japanese_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the improvement step!")
        self.console.new_lines(1)
        self.agents.engineer.improve_source_code()
        self.console.new_lines(1)
