from __future__ import annotations

import re

from your_dev_team.core.Message import Message
from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agent import Agent, AgentRole, NEXT_COMMAND
from your_dev_team.core.steps import step_prompts


class Engineer(Agent):
    def __init__(self, storages: Storages) -> None:
        super().__init__(AgentRole.ENGINEER, storages)

    def generate_source_code(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.generate_source_code_template.format(
                    specifications=self.storages.docs["specifications.md"],
                    technology_stack=self.storages.docs["technology_stack.md"],
                    directory_layout=self.storages.docs["layout_directory.md"],
                ),
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        files = Message.parse_message(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.src[file_name] = file_content

    def generate_entrypoint(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.generate_entrypoint_template.format()
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.src["run.sh"] = "\n".join(match.group(1) for match in matches)

    def improve_source_code(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.improve_source_code_template.format()
            )
        )
        for file_name, file_str in self._get_code_strings().items():
            self._console.print(
                f"Adding file {file_name} to the prompt...", style="blue"
            )
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            self.messages.append(Message.create_system_message(f"{code_input}"))

        response = self.ask(
            "What would you like to update?", require_answer=False, default_value=None
        )
        if response is not None:
            self.messages.append(Message.create_system_message(response))
        else:
            return

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        files = Message.parse_message(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.src[file_name] = file_content

    def _get_code_strings(self) -> dict[str, str]:
        return self.storages.src.recursive_file_search()
