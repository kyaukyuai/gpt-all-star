from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class Deployment(Step):
    def __init__(self, agents: Agents, japanese_mode: bool, auto_mode: bool) -> None:
        super().__init__(agents, japanese_mode, auto_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the deployment step!")
        self.console.new_lines(1)
        self.agents.copilot.push_to_git_repository()
        self.console.new_lines(1)
