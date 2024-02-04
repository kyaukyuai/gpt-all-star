from rich.table import Table
from gpt_all_star.cli.console_terminal import MAIN_COLOR

from gpt_all_star.core.message import Message
from gpt_all_star.core.agents import agents
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.steps.step import Step
from gpt_all_star.tool.text_parser import TextParser


class TeamBuilding(Step):
    def __init__(
        self, agents: agents, japanese_mode: bool, auto_mode: bool, debug_mode: bool
    ) -> None:
        super().__init__(agents, japanese_mode, auto_mode, debug_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's start by building a team!")
        self.console.new_lines()
        self._introduce_agent(self.agents.product_owner, AgentRole.PRODUCT_OWNER)
        self._introduce_agent(self.agents.engineer, AgentRole.ENGINEER)
        self._introduce_agent(self.agents.architect, AgentRole.ARCHITECT)
        self._introduce_agent(self.agents.designer, AgentRole.DESIGNER)
        self._introduce_agent(self.agents.qa_engineer, AgentRole.QA_ENGINEER)
        self._introduce_agent(self.agents.project_manager, AgentRole.PROJECT_MANAGER)
        self.console.new_lines()
        self.agents.copilot.state("Ok, we have a team now!")
        self._display_team_members()

    def _introduce_agent(self, agent: Agent, role: AgentRole) -> None:
        self.agents.copilot.state(f"Please introduce the {role.name}.")
        agent.name = self.agents.copilot.ask(
            f"What is the name of the {role.name}?",
            is_required=False,
            default=agent.name,
        )
        agent.profile = self.agents.copilot.ask(
            f"What is the profile of the {role.name}?",
            is_required=False,
            default=agent.profile,
        )
        agent.profile += "\nAny instruction you get that is labeled as **IMPORTANT**, you follow strictly."
        if self.japanese_mode:
            agent.profile += "\n**IMPORTANT: 必ず日本語で書いて下さい**"
        agent.messages = [Message.create_system_message(agent.profile)]

    def _display_team_members(self) -> None:
        table = Table(
            show_header=True, header_style=f"{MAIN_COLOR}", title="Team Members"
        )
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Profile")
        team_members = [
            agent
            for agent in vars(self.agents).values()
            if agent.role != AgentRole.COPILOT
        ]
        for member in team_members:
            table.add_row(
                member.name,
                member.role.name,
                TextParser.cut_last_n_lines(
                    member.profile, 2 if self.japanese_mode else 1
                ),
            )
        self.console.print(table)
        self.console.new_lines(1)
