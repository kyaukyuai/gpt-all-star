from __future__ import annotations

from helpers.Agent import Agent
from helpers.AgentConversation import AgentConversation


class ProductOwner(Agent):
    def __init__(self, project) -> None:
        """ProductOwner constructor

        :param project: Instance of the Project class
        """
        super().__init__('product_owner', project)
        self.agent_conversation: AgentConversation = AgentConversation(self)

    def get_project_description(self):
        self.project.current_step = 'project_description'
        self.agent_conversation.next(self.agent_conversation.messages, "")
