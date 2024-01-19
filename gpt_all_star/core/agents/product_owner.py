from __future__ import annotations

from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps import step_prompts


class ProductOwner(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str = "product_owner",
        profile: str = AgentRole.default_profile()[AgentRole.PRODUCT_OWNER].format(),
    ) -> None:
        super().__init__(AgentRole.PRODUCT_OWNER, storages, name, profile)

    def clarify_instructions(self) -> None:
        self.messages.append(
            Message.create_system_message(
                step_prompts.clarify_instructions_template.format(
                    instructions=self._get_instructions()
                )
            )
        )

        self._execute(
            "Answer in text, or proceed to the next step, type `{}`".format(
                NEXT_COMMAND
            ),
            "Make your own simplest assumptions possible and state them explicitly,"
            " **finally please answer 'It's clear!'**",
        )

    def _get_instructions(self) -> str:
        return (
            self.storages.origin["instructions"]
            if self.storages.origin.get("instructions") is not None
            else self.ask("What application do you want to generate?", self.role)
        )

    def summarize_specifications(self) -> None:
        self.messages.append(
            Message.create_system_message(
                step_prompts.summarize_specifications_template.format()
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs["specifications.md"] = file[1]
        self.state("Here are the specifications:")
        self.output_md(self.storages.docs["specifications.md"])
