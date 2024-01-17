from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agent import Agent, AgentRole


class Designer(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str = "designer",
        profile: str = AgentRole.default_profile()[AgentRole.DESIGNER].format(),
    ) -> None:
        super().__init__(AgentRole.DESIGNER, storages, name, profile)
