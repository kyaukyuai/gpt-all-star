from core.Storage import Storages
from core.agents.Agents import Agents
from core.steps.Step import Step


class Development(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        self.agents.engineer.generate_sourcecode()
        self.agents.engineer.generate_entrypoint()
