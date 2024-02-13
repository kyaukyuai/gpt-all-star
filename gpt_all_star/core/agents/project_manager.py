from __future__ import annotations

from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.storage import Storages


class ProjectManager(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.PROJECT_MANAGER, storages, debug_mode, name, profile)
