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
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.ARCHITECT, storages, debug_mode, name, profile)

    def create_system_design(self, review_mode: bool = False) -> None:
        self._create_technologies_list(review_mode)
        self._create_urls_list(review_mode)
        self._create_files_list(review_mode)

    def _create_technologies_list(self, review_mode: bool = False):
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
            review_mode=review_mode,
        )

        self.store_md("technologies", self.latest_message_content())

    def _create_urls_list(self, review_mode: bool = False):
        message = Message.create_system_message(
            create_urls_list_template.format(format=output_format)
        )
        self.messages.append(message)

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            review_mode=review_mode,
        )

        self.store_md("pages", self.latest_message_content())

    def _create_files_list(self, review_mode: bool = False):
        message = Message.create_system_message(
            create_files_list_template.format(format=output_format)
        )
        self.messages.append(message)

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            review_mode=review_mode,
        )

        self.store_md("files", self.latest_message_content())
