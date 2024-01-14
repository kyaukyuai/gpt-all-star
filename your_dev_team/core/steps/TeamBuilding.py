from rich.table import Table
from your_dev_team.core.agents import Agents
from your_dev_team.core.agents.Agent import AgentRole
from your_dev_team.core.steps.Step import Step


class TeamBuilding(Step):
    def __init__(self, agents: Agents) -> None:
        super().__init__(agents)

    def run(self) -> None:
        self.agents.copilot.state("Let's start by building a team!")
        self.console.new_lines(1)
        self._introduce_agent(self.agents.product_owner, AgentRole.PRODUCT_OWNER)
        self._introduce_agent(self.agents.engineer, AgentRole.ENGINEER)
        self._introduce_agent(self.agents.architect, AgentRole.ARCHITECT)
        self.console.new_lines(1)
        self.agents.copilot.state("Ok, we have a team now!")
        self._display_team_members()

    def _introduce_agent(self, agent, role: AgentRole) -> None:
        self.agents.copilot.state(f"Please introduce the {role.name.lower()}.")
        agent.name = self.agents.copilot.ask(
            f"What is the name of the {role.name.lower()}?",
            require_answer=False,
            default_value=AgentRole.default_name()[role],
        )
        agent.profile = self.agents.copilot.ask(
            f"What is the profile of the {role.name.lower()}?",
            require_answer=False,
            default_value=AgentRole.default_profile()[role].format(),
        )

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
