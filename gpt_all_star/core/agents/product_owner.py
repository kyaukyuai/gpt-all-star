from __future__ import annotations

from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.storage import Storages
from gpt_all_star.helper.config_loader import load_configuration

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

    def load_instructions(
        self, file_path: str = "./gpt_all_star/instructions.yml"
    ) -> dict:
        return load_configuration(file_path)

    def get_instructions(self) -> str:
        instructions = self.load_instructions()
        instruction = instructions.get("instruction")
        if instruction:
            return instruction
        return self.ask(
            "What application do you want to build? Please describe it in as much detail as possible."
        )

    def get_app_type(self) -> str:
        instructions = self.load_instructions()
        app_type = instructions.get("app_type")
        if app_type:
            return app_type
        return self.present_choices(
            "What type of application do you want to build?",
            APP_TYPES,
            default=1,
        )
