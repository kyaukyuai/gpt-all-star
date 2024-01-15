from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.steps.Step import Step


class SystemDesign(Step):
    def __init__(self, agents: Agents, mode) -> None:
        super().__init__(agents, mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the system design step!")
        self.console.new_lines(1)
        self.agents.architect.state("How about the following?")
        self.agents.architect.list_technology_stack()
        self.console.new_lines(1)
        self.agents.architect.state("How about the following?")
        self.agents.architect.layout_directory()
        self.console.new_lines(1)
