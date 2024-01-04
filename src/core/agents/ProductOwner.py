from __future__ import annotations

from langchain_core.messages import BaseMessage

from core.Storage import Storages
from core.agents.Agent import Agent, AgentRole, NEXT_COMMAND
from core.Message import Message
from prompts.steps import step_prompts


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

        user_input = None
        count = 0

        while "nothing to clarify" not in self.latest_message_content().lower():
            if count > 0:
                self.terminal.new_lines(2)
                user_input = self.terminal.ask_user(
                    f"Answer in text, or proceed to the next step, type `{NEXT_COMMAND}`")
                if user_input == NEXT_COMMAND:
                    self.chat(
                        "Make your own assumptions and state them explicitly,"
                        " **finally please answer 'It's clear!'**")
                    self.terminal.new_lines(1)
                    break

            self.chat(user_input)
            count += 1

        self.storages.memory['clarify_instructions'] = Message.serialize_messages(self.messages)

    def _get_instructions(self) -> str:
        return (
            self.storages.origin['instructions']
            if self.storages.origin.get('instructions') is not None
            else self.terminal.ask_user("What application do you want to generate?")
        )

    def summarize_specifications(self) -> None:
        self.messages.extend(self._get_clarified_instructions())
        self.messages.append(
            Message.create_system_message(
                step_prompts.summarize_specifications_template.format()
            )
        )

        user_input = None
        count = 0

        while True:
            if count > 0:
                self.terminal.new_lines(1)
                user_input = self.terminal.ask_user(
                    f"Do you want to add any features or changes?"
                    f" If yes, describe it here and if no, just type `{NEXT_COMMAND}`"
                )
                if user_input == NEXT_COMMAND:
                    break

            self.chat(user_input)
            count += 1

        self.storages.memory[self.__class__.__name__.lower()] = Message.serialize_messages(
            self.messages)
        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.memory['specification.md'] = file[1]

    def _get_clarified_instructions(self) -> list[BaseMessage]:
        return Message.deserialize_messages(
            self.storages.memory['clarify_instructions']) if self.is_initialized() else []
