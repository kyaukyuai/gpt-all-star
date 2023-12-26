from __future__ import annotations

from helpers.AgentRole import AgentRole
from helpers.Agent import Agent
from helpers.AgentConversation import AgentConversation
from logger.logger import logger
from utils.prompts import get_prompt


class ProductOwner(Agent):
    def __init__(self, project) -> None:
        """ProductOwner constructor

        :param project: Instance of the Project class
        """
        super().__init__(AgentRole.PRODUCT_OWNER, project)
        self.agent_conversation: AgentConversation = AgentConversation(self)

    def get_project_description(self, specification: str):
        self.project.current_step = 'project_description'
        clarify_message = self.agent_conversation.create_system_message(get_prompt('steps/clarify'))
        logger.info(f"step prompt is '{clarify_message}'")
        self.agent_conversation.messages.append(clarify_message)
        user_input = self.agent_conversation.create_human_message(specification)
        logger.info(f"original specification is '{specification}'")
        self.agent_conversation.messages.append(user_input)
