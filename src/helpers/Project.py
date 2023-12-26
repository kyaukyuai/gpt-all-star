from __future__ import annotations
from pprint import pprint

from rich.console import Console

from helpers.agents.ProductOwner import ProductOwner
from utils.prompt_toolkit import get_input


class Project:
    def __init__(
            self,
            args: dict,
            name: str | None = None,
            description: str | None = None,
            user_stories: str | None = None,
            user_tasks: str | None = None,
            architecture: str | None = None,
            development_plan: str | None = None,
            current_step: str | None = None
    ) -> None:
        self.product_owner: ProductOwner | None = None
        self.args: dict = args
        self.current_step: str | None = current_step
        self.name: str | None = name
        self.description: str | None = description
        self.user_stories: str | None = user_stories
        self.user_tasks: str | None = user_tasks
        self.architecture: str | None = architecture
        self.development_plan: str | None = development_plan

        self._print_settings()

        self.console: Console = Console()

    def _print_settings(self) -> None:
        pprint(
            f"Project setting is set with args: {self.args},"
            f" name: {self.name}, description: {self.description}, user_stories: {self.user_stories},"
            f" user_tasks: {self.user_tasks}, architecture: {self.architecture},"
            f" development_plan: {self.development_plan}, current_step: {self.current_step}"
        )

    def start(self) -> None:
        pprint("Project started!")

        self.product_owner = ProductOwner(self)
        self.product_owner.print_project()
        self.product_owner.print_role()
        # self.product_owner.get_project_description()

        while True:
            try:
                self.execute()
            except KeyboardInterrupt:
                break

    def execute(self):
        messages = self.product_owner.agent_conversation.messages
        user_input = get_input('project.history', set())
        self.product_owner.agent_conversation.next(messages, user_input)
        self.console.print()
