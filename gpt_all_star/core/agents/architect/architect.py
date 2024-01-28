from gpt_all_star.core.agents.architect.output_format import output_format
from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.agents.architect.create_technologies_list_prompt import (
    create_technologies_list_template,
)
from gpt_all_star.core.agents.architect.create_urls_list_prompt import (
    create_urls_list_template,
)
from gpt_all_star.core.agents.architect.create_files_list_prompt import (
    create_files_list_template,
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
        self._create_technologies_list(auto_mode)
        self._create_urls_list(auto_mode)
        self._create_files_list(auto_mode)

    def _create_technologies_list(self, auto_mode: bool = False):
        self.state("How about the following?")

        message = Message.create_system_message(
            create_technologies_list_template.format(
                specifications=self.storages.docs["specifications.md"],
                format=output_format,
            )
        )
        self.messages.append(message)

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        self.store_md("technologies", self.latest_message_content())

    def _create_urls_list(self, auto_mode: bool = False):
        self.state("How about the following?")

        message = Message.create_system_message(
            create_urls_list_template.format(
                specifications=self.storages.docs["specifications.md"],
                format=output_format,
            )
        )
        self.messages.append(message)

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        self.store_md("pages", self.latest_message_content())

    def _create_files_list(self, auto_mode: bool = False):
        self.state("How about the following?")

        message = Message.create_system_message(
            create_files_list_template.format(
                specifications=self.storages.docs["specifications.md"],
                technologies=self.storages.docs["technologies.md"],
                pages=self.storages.docs["pages.md"],
                format=output_format,
            )
        )
        self.messages.append(message)

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        self.store_md("files", self.latest_message_content())
