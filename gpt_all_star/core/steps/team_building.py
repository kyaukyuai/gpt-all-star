from rich.table import Table

from gpt_all_star.core.message import Message
from gpt_all_star.core.agents import agents
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.steps.step import Step


class TeamBuilding(Step):
    def __init__(self, agents: agents, japanese_mode: bool, auto_mode: bool) -> None:
        super().__init__(agents, japanese_mode, auto_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's start by building a team!")
        self.console.new_lines(1)
        self._introduce_agent(self.agents.product_owner, AgentRole.PRODUCT_OWNER)
        self._introduce_agent(self.agents.engineer, AgentRole.ENGINEER)
        self._introduce_agent(self.agents.architect, AgentRole.ARCHITECT)
        self._introduce_agent(self.agents.designer, AgentRole.DESIGNER)
        self.console.new_lines(1)
        self.agents.copilot.state("Ok, we have a team now!")
        self._display_team_members()

    def _introduce_agent(self, agent: Agent, role: AgentRole) -> None:
        self.agents.copilot.state(f"Please introduce the {role.name.lower()}.")
        agent.name = self.agents.copilot.ask(
            f"What is the name of the {role.name.lower()}?",
            is_required=False,
            default=agent.name,
        )
        agent.profile = self.agents.copilot.ask(
            f"What is the profile of the {role.name.lower()}?",
            is_required=False,
            default=agent.profile,
        )
        if self.japanese_mode:
            agent.profile = agent.profile + "**必ず日本語で書いて下さい**"
        agent.messages = [Message.create_system_message(agent.profile)]

    def _display_team_members(self) -> None:
        table = Table(show_header=True, header_style="#FFB001", title="Team Members")
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Profile")
        for agent in vars(self.agents).values():
            if agent.role != AgentRole.COPILOT:
                table.add_row(agent.name, agent.role.name, agent.profile)
        self.console.print(table)
        self.console.new_lines(1)
