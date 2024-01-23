from __future__ import annotations

from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole


class QAEngineer(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.QA_ENGINEER, storages, name, profile)
