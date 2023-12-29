from __future__ import annotations

import os.path
from pathlib import Path

from langchain_core.messages import BaseMessage
from rich.console import Console

from helpers.Message import Message
from helpers.Step import StepType, STEPS
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
            current_step: str | None = None
    ) -> None:
        self.args: dict = args
        self.name: str | None = name
        self.description: str | None = description
        self.current_step: str | None = current_step

        self.step_type = StepType.DEFAULT
        self.console: Console = Console()

        self.storage = Storage(Path(os.path.abspath('projects/example')).absolute())
        self.output = Storage(Path(os.path.abspath('projects/example/output')).absolute())

        self.product_owner: ProductOwner = ProductOwner(self)

    def start(self) -> None:
        try:
            for step in STEPS[self.step_type]:
                try:
                    self.execute(step)
                except Exception as e:
                    logger.error(f"Failed to execute step {step}. Reason: {str(e)}")
                    raise e
        except KeyboardInterrupt:
            logger.info("Interrupt received! Stopping...")
            pass

    def execute(self, step: str) -> list[BaseMessage] | str:
        self.console.rule(f"【 step: {step.capitalize()} 】")
        if step == 'clarify':
            self.product_owner.get_project_description(self.storage['specification.md'])

            user_input = None
            response = ""
            count = 0

            while "nothing to clarify" not in response.lower():
                if count > 0:
                    user_input = get_input('project.history', set())
                    if user_input == NEXT_COMMAND:
                        self.product_owner.chat(
                            "Make your own assumptions and state them explicitly, and please answer 'Nothing to "
                            "clarify'")
                        self.console.print()
                        break

                self.product_owner.chat(user_input)

                response = self.product_owner.latest_message_content()
                logger.info(f"response: {response}")

                count += 1
                self.console.print()
                self.console.print(f"Answer in text, or o proceed to the next step, type `{NEXT_COMMAND}`",
                                   style='bold yellow')
                self.console.print()

            self.output[step] = Message.serialize_messages(self.product_owner.messages)
            return self.product_owner.messages

        elif step == 'update_specification':
            self.product_owner.update_project_specification(None)
            self.product_owner.chat(None)

            response = self.product_owner.latest_message_content()
            logger.info(f"response: {response}")
            self.console.print()

            self.output[step] = Message.serialize_messages(self.product_owner.messages)
            file = Message.parse_message(self.product_owner.latest_message_content())[0]
            self.output[file[0]] = file[1]
            return self.product_owner.messages

        self.console.print()
        return []
