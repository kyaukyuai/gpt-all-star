from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.agents.architect.list_technology_prompt import (
    list_technology_template,
)
from gpt_all_star.core.agents.architect.list_page_prompt import (
    list_page_template,
)
from gpt_all_star.core.agents.architect.list_file_prompt import (
    list_file_template,
)


class Architect(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.ARCHITECT, storages, name, profile)

    def create_system_design(self, auto_mode: bool = False) -> None:
        self._list_technology(auto_mode)
        self._list_page(auto_mode)
        self._list_file(auto_mode)

    def _list_technology(self, auto_mode: bool = False):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                list_technology_template.format(
                    specifications=self.storages.docs["specifications.md"]
                )
            )
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        self.store_md("technologies", self.latest_message_content())

    def _list_page(self, auto_mode: bool = False):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                list_page_template.format(
                    specifications=self.storages.docs["specifications.md"]
                )
            )
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        self.store_md("pages", self.latest_message_content())

    def _list_file(self, auto_mode: bool = False):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                list_file_template.format(
                    specifications=self.storages.docs["specifications.md"],
                    technologies=self.storages.docs["technologies.md"],
                    pages=self.storages.docs["pages.md"],
                )
            )
        )

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        self.store_md("files", self.latest_message_content())
