from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.steps.Step import Step


class Development(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the development step!")
        self.console.new_lines(1)
        self.agents.engineer.state("How about the following?")
        self.agents.engineer.generate_source_code()
        self.agents.engineer.generate_entrypoint()
        self.console.new_lines(1)
