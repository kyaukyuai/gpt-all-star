import re

from langchain_core.messages import BaseMessage

from core.Message import Message
from core.Storage import Storages
from core.agents.Agents import Agents
from core.steps.Step import Step
from logger.logger import logger


class Development(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> list[BaseMessage]:
        self.agents.engineer.develop(self.storages.memory['specification.md'])
        self.agents.engineer.chat(None)

        response = self.agents.engineer.latest_message_content()
        logger.info(f"response: {response}")
        self.console.print()

        self.storages.memory['development'] = Message.serialize_messages(
            self.agents.engineer.messages)

        files = Message.parse_message(self.agents.engineer.latest_message_content())
        for file_name, file_content in files:
            self.storages.src[file_name] = file_content

        self.agents.engineer.generate_entrypoint()
        self.agents.engineer.chat(None)

        response = self.agents.engineer.latest_message_content()
        logger.info(f"response: {response}")
        self.console.print()

        self.storages.memory['generate_entrypoint'] = Message.serialize_messages(
            self.agents.engineer.messages)
        regex = r"```\S*\n(.+?)```"
        matches = re.finditer(regex, response, re.DOTALL)
        self.storages.src["run.sh"] = "\n".join(match.group(1) for match in matches)
        return self.agents.engineer.messages

    def _develop(self):
        pass

    def _generate_entrypoint(self):
        pass
