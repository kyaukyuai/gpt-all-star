from __future__ import annotations

from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.agents.product_owner.clarify_instruction_prompt import (
    clarify_instructions_template,
    auto_clarify_instructions_template,
)
from gpt_all_star.core.agents.product_owner.summarize_specification_prompt import (
    summarize_specifications_template,
)
from gpt_all_star.core.message import Message
from gpt_all_star.tool.text_parser import TextParser

APP_TYPES = ["Client-Side Web Application", "Full-Stack Web Application"]


class ProductOwner(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER, storages, name, profile)

    def create_specifications(self, auto_mode: bool = False) -> None:
        self._clarify_instructions(auto_mode)
        self._summarize_specifications(auto_mode)

    def _clarify_instructions(self, auto_mode: bool = False) -> None:
        instructions = self._get_instructions()
        app_type = self._get_app_type()

        clarification_method = (
            self._clarify_instructions_auto
            if auto_mode
            else self._clarify_instructions_manual
        )
        clarification_method(instructions, app_type)

        self._summarize_specifications(auto_mode)

    def _clarify_instructions_auto(self, instructions: str, app_type: str) -> None:
        message = Message.create_system_message(
            auto_clarify_instructions_template.format(
                instructions=instructions,
                app_type=app_type,
            )
        )
        self.messages.append(message)
        self.chat()
        self.console.new_lines(2)

    def _clarify_instructions_manual(self, instructions: str, app_type: str) -> None:
        message = Message.create_system_message(
            clarify_instructions_template.format(
                instructions=instructions,
                app_type=app_type,
            )
        )
        self.messages.append(message)
        self.execute(
            "Answer in text, or proceed to the next step, type `{}`".format(
                NEXT_COMMAND
            ),
            "Assume the ambiguity as the simplest possible specification for building the MVP(Minimum Viable Product) and state them clearly.",
        )

    def _get_instructions(self) -> str:
        return self.storages.root.get("instructions") or self.ask(
            "What application do you want to build? Please describe it in as much detail as possible."
        )

    def _get_app_type(self) -> str:
        return self.present_choices(
            "What type of application do you want to build?",
            APP_TYPES,
            default=1,
        )

    def _summarize_specifications(self, auto_mode: bool = False) -> None:
        self.state("How about the following?")

        message = Message.create_system_message(
            summarize_specifications_template.format()
        )

        self.messages.append(message)

        self.execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
            auto_mode=auto_mode,
        )

        file = TextParser.parse_code_from_text(self.latest_message_content())[0]
        self.storages.docs["specifications.md"] = file[1]

        self.state("There are the specifications to build the application:")
        self.output_md(self.storages.docs["specifications.md"])
