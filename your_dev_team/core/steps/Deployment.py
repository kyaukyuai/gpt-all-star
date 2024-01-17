from your_dev_team.core.agents.agents import Agents
from your_dev_team.core.steps.step import Step


class Deployment(Step):
    def __init__(self, agents: Agents, japanese_mode) -> None:
        super().__init__(agents, japanese_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the deployment step!")
        self.console.new_lines(1)
        self.agents.copilot.push_to_git_repository()
        self.console.new_lines(1)
