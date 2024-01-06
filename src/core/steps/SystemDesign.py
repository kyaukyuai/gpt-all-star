from core.Storage import Storages
from core.agents.Agents import Agents
from core.steps.Step import Step


class SystemDesign(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        self.agents.architect.list_technology_stack()
