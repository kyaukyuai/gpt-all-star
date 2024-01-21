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
        name: str = "architect",
        profile: str = AgentRole.default_profile()[AgentRole.ARCHITECT].format(),
    ) -> None:
        super().__init__(AgentRole.ARCHITECT, storages, name, profile)

    def design_system(self):
        self._list_technology()
        self._list_page()
        self._list_file()

    def _list_technology(self):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                list_technology_template.format(
                    specifications=self.storages.docs["specifications.md"]
                )
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs["technology.md"] = file[1]
        self.state("These are the technologies used to build the application:")
        self.output_md(self.storages.docs["technology.md"])

    def _list_page(self):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                list_page_template.format(
                    specifications=self.storages.docs["specifications.md"]
                )
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs["page.md"] = file[1]
        self.state("These are the pages required by the application:")
        self.output_md(self.storages.docs["page.md"])

    def _list_file(self):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                list_file_template.format(
                    specifications=self.storages.docs["specifications.md"],
                    technology=self.storages.docs["technology.md"],
                    page=self.storages.docs["page.md"],
                )
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs["file.md"] = file[1]
        self.state("These are the files required by the application:")
        self.output_md(self.storages.docs["file.md"])
