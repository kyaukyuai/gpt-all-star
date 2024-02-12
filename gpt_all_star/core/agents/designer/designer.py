from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole


class Designer(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.DESIGNER, storages, debug_mode, name, profile)
