from __future__ import annotations

from langchain_core.messages import BaseMessage

from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agent import Agent, AgentRole, NEXT_COMMAND
from your_dev_team.core.Message import Message
from your_dev_team.core.steps import step_prompts


class ProductOwner(Agent):
    def __init__(self, storages: Storages) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER, storages)

    def clarify_instructions(self) -> None:
        self.messages.append(
            Message.create_system_message(
                step_prompts.clarify_instructions_template.format(
                    instructions=self._get_instructions()
                )
            )
        )

        self._execute(
            "Answer in text, or proceed to the next step, type `{}`".format(NEXT_COMMAND),
            "Make your own simplest assumptions possible and state them explicitly,"
            " **finally please answer 'It's clear!'**"
        )

        self.storages.memory['clarify_instructions'] = Message.serialize_messages(self.messages)

    def _get_instructions(self) -> str:
        return (
            self.storages.origin['instructions']
            if self.storages.origin.get('instructions') is not None
            else self.terminal.ask_user("What application do you want to generate?", self.role)
        )

    def summarize_specifications(self) -> None:
        self.messages.extend(self._get_clarified_instructions())
        self.messages.append(
            Message.create_system_message(
                step_prompts.summarize_specifications_template.format()
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND),
        )

        self.storages.memory['summarize_specifications'] = Message.serialize_messages(
            self.messages)
        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs['specifications.md'] = file[1]

    def _get_clarified_instructions(self) -> list[BaseMessage]:
        return Message.deserialize_messages(
            self.storages.memory['clarify_instructions']) if self.is_initialized() else []
