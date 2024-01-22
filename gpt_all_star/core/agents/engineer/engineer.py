from __future__ import annotations

import re

from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.agents.engineer.create_source_code_prompt import (
    create_source_code_template,
)
from gpt_all_star.core.agents.engineer.create_entrypoint_prompt import (
    create_entrypoint_template,
)
from gpt_all_star.core.agents.engineer.create_readme_prompt import (
    create_readme_template,
)
from gpt_all_star.core.steps import step_prompts


class Engineer(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.ENGINEER, storages, name, profile)

    def create_source_code(self, auto_mode: bool = False):
        self.state("How about the following?")

        self.messages.append(
            Message.create_system_message(
                create_source_code_template.format(
                    specifications=self.storages.docs["specifications.md"],
                    technology=self.storages.docs["technology.md"],
                    page=self.storages.docs["page.md"],
                    file=self.storages.docs["file.md"],
                ),
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        files = Message.parse_message(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.root[file_name] = file_content

        self._create_entrypoint(auto_mode)
        self._create_readme(auto_mode)

    def _create_entrypoint(self, auto_mode: bool = False):
        self.messages.append(
            Message.create_system_message(create_entrypoint_template.format())
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.root["run.sh"] = "\n".join(match.group(1) for match in matches)

    def _create_readme(self, auto_mode: bool = False):
        self.messages.append(
            Message.create_system_message(create_readme_template.format())
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.root["README.md"] = "\n".join(match.group(1) for match in matches)

    def improve_source_code(self, auto_mode: bool = False):
        self.messages.append(
            Message.create_system_message(
                step_prompts.improve_source_code_template.format()
            )
        )
        for file_name, file_str in self.storages.root.recursive_file_search().items():
            self._console.print(
                f"Adding file {file_name} to the prompt...", style="blue"
            )
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            self.messages.append(Message.create_system_message(f"{code_input}"))

        response = self.ask(
            "What would you like to update?", is_required=False, default=None
        )
        if response is not None:
            self.messages.append(Message.create_system_message(response))
        else:
            return

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        files = Message.parse_message(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.root[file_name] = file_content
