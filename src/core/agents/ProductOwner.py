from __future__ import annotations

from langchain_core.messages import BaseMessage

from core.Storage import Storages
from core.agents.Agent import Agent, AgentRole, NEXT_COMMAND
from core.Message import Message
from prompts.prompts import get_prompt
from prompts.steps import step_prompts


class ProductOwner(Agent):
    def __init__(self, storages: Storages) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER, storages)

    def clarify_specification(self) -> None:
        self.messages.append(
            Message.create_system_message(
                step_prompts.clarify_template.format(instructions=self._get_instructions())
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

        self.storages.memory['clarify_specification'] = Message.serialize_messages(self.messages)

    def _get_instructions(self) -> str:
        return (
            self.storages.origin['instructions']
            if self.storages.origin.get('instructions') is not None
            else self.terminal.ask_user("What application do you want to generate?")
        )

    def create_specification(self, messages: list[BaseMessage] | None) -> None:
        if messages is not None:
            self.messages += messages

        self.messages.append(Message.create_system_message(get_prompt('steps/update_specification')))
