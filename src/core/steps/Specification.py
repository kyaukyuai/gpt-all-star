from core.agents import Agents
from core.steps.Step import Step
from core.Storage import Storages


class Specification(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        self.agents.product_owner.clarify_instructions()
        self.agents.product_owner.summarize_specifications()
