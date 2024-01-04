from __future__ import annotations

from langchain_core.messages import BaseMessage

from core.agents.Agent import Agent, AgentRole, NEXT_COMMAND
from core.Message import Message
from logger.logger import logger
from prompts.prompts import get_prompt
from prompts.steps import step_prompts


class ProductOwner(Agent):
    def __init__(self) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER)

    def clarify_specification(self, instructions: str) -> list[BaseMessage]:
        self.messages.append(
            Message.create_system_message(
                step_prompts.clarify_template.format(instructions=instructions)
            )
        )

        user_input = None
        response = ""
        count = 0

        while "nothing to clarify" not in response.lower():
            if count > 0:
                self.terminal.new_lines(2)
                user_input = self.terminal.ask_user(
                    f"Answer in text, or o proceed to the next step, type `{NEXT_COMMAND}`")
                if user_input == NEXT_COMMAND:
                    self.chat(
                        "Make your own assumptions and state them explicitly,"
                        " **finally please answer 'It's clear!'**")
                    self.terminal.new_lines(1)
                    break

            self.chat(user_input)

            response = self.latest_message_content()
            logger.info(f"response: {response}")
            count += 1

        return self.messages

    def create_specification(self, messages: list[BaseMessage] | None) -> None:
        if messages is not None:
            self.messages += messages

        self.messages.append(Message.create_system_message(get_prompt('steps/update_specification')))
