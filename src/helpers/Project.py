from __future__ import annotations

import os.path
from pathlib import Path

from langchain_core.messages import BaseMessage
from rich.console import Console

from helpers.AgentConversation import AgentConversation
from helpers.Storage import Storage
from helpers.agents.ProductOwner import ProductOwner
from logger.logger import logger
from utils.prompt_toolkit import get_input

NEXT_COMMAND = "next"


class Project:
    def __init__(
            self,
            args: dict,
            name: str | None = None,
            description: str | None = None,
            user_stories: str | None = None,
            user_tasks: str | None = None,
            architecture: str | None = None,
            development_plan: str | None = None,
            current_step: str | None = None
    ) -> None:
        self.product_owner: ProductOwner | None = None
        self.args: dict = args
        self.current_step: str | None = current_step
        self.name: str | None = name
        self.description: str | None = description
        self.user_stories: str | None = user_stories
        self.user_tasks: str | None = user_tasks
        self.architecture: str | None = architecture
        self.development_plan: str | None = development_plan

        self.console: Console = Console()
        self.storage = Storage(Path(os.path.abspath('projects/example')).absolute())
        self.output = Storage(Path(os.path.abspath('projects/example/output')).absolute())

    def start(self) -> None:
        self.product_owner = ProductOwner(self)
        self.product_owner.print_project()
        self.product_owner.print_role()

        try:
            for step in ['clarify', 'update_specification']:
                self.console.rule(f"【 step: {step.capitalize()} 】")
                messages = self.execute(step)
                self.output[step] = AgentConversation.serialize_messages(messages)
                if step == 'update_specification':
                    md = messages[-1].content
                    self.output['specification.md'] = md
        except KeyboardInterrupt:
            pass

    def execute(self, step: str) -> list[BaseMessage] | str:
        if step == 'clarify':
            self.product_owner.get_project_description(self.storage['specification.md'])
            while True:
                messages: list[BaseMessage] = []
                user_input = get_input('project.history', set())
                if user_input == NEXT_COMMAND:
                    break

                conversation = self.product_owner.agent_conversation
                messages = conversation.next(conversation.messages, user_input)
                conversation.messages = messages

                response = conversation.messages[-1].content.strip()
                logger.info(f"response: {response}")
                self.console.print()

                if "nothing to clarify" in response.lower():
                    break

            return messages

        elif step == 'update_specification':
            self.product_owner.update_project_specification(
                AgentConversation.deserialize_messages(self.output['clarify']))
            conversation = self.product_owner.agent_conversation
            messages = conversation.next(conversation.messages, None)
            conversation.messages = messages

            response = conversation.messages[-1].content.strip()
            logger.info(f"response: {response}")
            self.console.print()

            return messages

        self.console.print()
        return []
