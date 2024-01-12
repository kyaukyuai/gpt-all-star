from your_dev_team.core.agents import Agents
from your_dev_team.core.steps.Step import Step
from your_dev_team.core.Storage import Storages


class Specification(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the specification step!")
        self.console.new_lines(1)
        self.agents.product_owner.clarify_instructions()
        self.agents.product_owner.state("How about the following?")
        self.agents.product_owner.summarize_specifications()
        self.console.new_lines(1)
