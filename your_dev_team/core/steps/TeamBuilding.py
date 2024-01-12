from your_dev_team.core.agents import Agents
from your_dev_team.core.steps.Step import Step
from your_dev_team.core.Storage import Storages


class TeamBuilding(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> None:
        self.agents.copilot.build_team_members()
