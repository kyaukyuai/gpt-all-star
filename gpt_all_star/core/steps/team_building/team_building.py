from gpt_all_star.core.steps.team_building.team_table import TeamTable
from rich.table import Table

from gpt_all_star.cli.console_terminal import MAIN_COLOR
from gpt_all_star.core.agents import agents
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.helper.config_loader import load_configuration
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
        agents_list = load_configuration("./gpt_all_star/agents.yml")
        if agents_list:
            for agent_info in agents_list:
                self._set_agent_attributes(agent_info)
        else:
            self._introduce_agents_manually()

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
        team_table = TeamTable()
        team_table.display_team_members([agent for agent in vars(self.agents).values() if agent.role != AgentRole.COPILOT])
