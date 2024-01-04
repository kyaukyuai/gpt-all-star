from langchain_core.messages import BaseMessage

from core.Message import Message
from core.Storage import Storages
from core.agents.Agent import Agent, AgentRole
from prompts.prompts import get_prompt


class Engineer(Agent):
    def __init__(self, storages: Storages) -> None:
        super().__init__(AgentRole.ENGINEER, storages)

    def develop(self, specification: str):
        self.messages.append(Message.create_system_message(get_prompt('steps/development')))
        self.messages.append(Message.create_human_message(specification))

    def generate_entrypoint(self):
        self.messages.append(Message.create_system_message(
            "You will get information about a codebase that is currently on disk in "
            "the current folder.\n"
            "From this you will answer with code blocks that includes all the necessary "
            "unix terminal commands to "
            "a) install dependencies "
            "b) run all necessary parts of the codebase (in parallel if necessary).\n"
            "Do not install globally. Do not use sudo.\n"
            "Do not explain the code, just give the commands.\n"
            "Do not use placeholders, use example values (like . for a folder argument) "
            "if necessary.\n"
        ))
