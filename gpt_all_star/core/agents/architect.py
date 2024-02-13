from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.storage import Storages


class Architect(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.ARCHITECT, storages, debug_mode, name, profile)
