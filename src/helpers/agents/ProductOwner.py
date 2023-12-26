from __future__ import annotations

import json
from pprint import pprint

from helpers.Agent import Agent
from helpers.AgentConversation import AgentConversation
from logger.logger import logger


class ProductOwner(Agent):
    def __init__(self, project) -> None:
        """ProductOwner constructor

        :param project: Instance of the Project class
        """
        super().__init__('product_owner', project)

    def get_project_description(self):
        self.project.current_step = 'project_description'
        agent_conversation = AgentConversation(self)
        agent_conversation.next(agent_conversation.messages, "")
