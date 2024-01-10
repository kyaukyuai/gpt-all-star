from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.steps.Step import Step


class SystemDesign(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        self.agents.architect.plan()
        self.agents.architect.list_technology_stack()
        self.agents.architect.layout_directory()
