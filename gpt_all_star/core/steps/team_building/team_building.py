import os

import yaml
from rich.table import Table

from gpt_all_star.cli.console_terminal import MAIN_COLOR
from gpt_all_star.core.agents import agents
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.helper.text_parser import TextParser


class TeamBuilding(Step):
    def __init__(
        self,
        agents: agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's start by building a team!")
        self.console.new_lines()
        self._introduce_agents()
        self.console.new_lines()
        self.agents.copilot.state("Ok, we have a team now!")
        self._display_team_members()

    def _introduce_agents(self) -> None:
        if os.path.exists("./gpt_all_star/agents.yml"):
            self._introduce_agents_from_file()
        else:
            self._introduce_agents_manually()

    def _introduce_agents_from_file(self) -> None:
        with open("./gpt_all_star/agents.yml", "r") as file:
            agents_list = yaml.safe_load(file)
        for agent_info in agents_list:
            self._set_agent_attributes(agent_info)

    def _set_agent_attributes(self, agent_info: dict) -> None:
        agent = getattr(self.agents, agent_info["role"])
        agent.name = agent_info["name"]
        agent.profile = agent_info["profile"]
        self._add_instructions_to_profile(agent)
        agent.messages = [Message.create_system_message(agent.profile)]

    def _add_instructions_to_profile(self, agent: Agent) -> None:
        agent.profile += "\nAny instruction you get that is labeled as **IMPORTANT**, you follow strictly."
        if self.japanese_mode:
            agent.profile += "\n**IMPORTANT: 必ず日本語で書いて下さい**"

    def _introduce_agents_manually(self) -> None:
        for role in AgentRole:
            if role != AgentRole.COPILOT:
                self._introduce_agent(getattr(self.agents, role.value), role)

    def _introduce_agent(self, agent: Agent, role: AgentRole) -> None:
        self.agents.copilot.state(f"Please introduce the {role.name}.")
        self._ask_agent_name(agent, role)
        self._ask_agent_profile(agent, role)
        self._add_instructions_to_profile(agent)
        agent.messages = [Message.create_system_message(agent.profile)]

    def _ask_agent_name(self, agent: Agent, role: AgentRole) -> None:
        agent.name = self.agents.copilot.ask(
            f"What is the name of the {role.name}?",
            is_required=False,
            default=agent.name,
        )

    def _ask_agent_profile(self, agent: Agent, role: AgentRole) -> None:
        agent.profile = self.agents.copilot.ask(
            f"What is the profile of the {role.name}?",
            is_required=False,
            default=agent.profile,
        )

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
