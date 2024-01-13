from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.steps.Step import Step


class Deployment(Step):
    def __init__(self, agents: Agents) -> None:
        super().__init__(agents)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the deployment step!")
        self.console.new_lines(1)
        self.agents.copilot.create_github_repo()
        self.agents.copilot.git_push()
        self.console.new_lines(1)
