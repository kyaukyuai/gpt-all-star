from __future__ import annotations

from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.storage import Storages

APP_TYPES = ["Client-Side Web Application", "Full-Stack Web Application"]


class ProductOwner(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER, storages, debug_mode, name, profile)

    def get_instructions(self) -> str:
        return self.storages.docs.get("instructions") or self.ask(
            "What application do you want to build? Please describe it in as much detail as possible."
        )

    def get_app_type(self) -> str:
        return self.present_choices(
            "What type of application do you want to build?",
            APP_TYPES,
            default=1,
        )
