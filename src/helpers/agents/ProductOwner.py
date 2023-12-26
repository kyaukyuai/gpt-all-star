from __future__ import annotations

from ..Agent import Agent
from ..AgentConversation import AgentConversation


class ProductOwner(Agent):
    def __init__(self, project) -> None:
        """ProductOwner constructor

        :param project: Instance of the Project class
        """
        super().__init__('product_owner', project)

    def get_project_description(self) -> AgentConversation:
        """Get Project description

        :return: Instance of the AgentConversation class
        """
        self.project.current_step = 'project_description'
        return AgentConversation(self)
