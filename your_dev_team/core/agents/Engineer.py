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
                    specifications=self.storages.docs['specifications.md'])
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND),
        )

        self.storages.memory['generate_source_code'] = Message.serialize_messages(self.messages)

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
                NEXT_COMMAND),
        )

        self.storages.memory['generate_entrypoint'] = Message.serialize_messages(
            self.messages)
        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, self.latest_message_content(), re.DOTALL)
        self.storages.src["run.sh"] = "\n".join(match.group(1) for match in matches)
