from gpt_all_star.core.agents.agent import AgentRole
from gpt_all_star.core.execution import planning_prompt
from gpt_all_star.core.team import Team


class TeamBuilding:
    def __init__(self):
        self.team = Team()

    def run(self, planning_prompt):
        self.assign_supervisor(planning_prompt)
        self.introduce_agents()
        self.display_team_members()

    def assign_supervisor(self, planning_prompt):
        self.team._assign_supervisor(planning_prompt)

    def introduce_agents(self):
        agents_list = self.team.storages().load_configuration("./gpt_all_star/agents.yml")
        if agents_list:
            for agent_info in agents_list:
                self.team._set_agent_attributes(agent_info)
        else:
            self.team._introduce_agents_manually()

    def display_team_members(self):
        table = self.team.tools.Table(
            show_header=True, header_style=f"{self.team.MAIN_COLOR}", title="Team Members"
        )
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Profile")
        team_members = [
            agent
            for agent in vars(self.team.agents).values()
            if agent.role != AgentRole.COPILOT
        ]
        for member in team_members:
            table.add_row(
                member.name,
                member.role.name,
                self.team.tools.TextParser.cut_last_n_lines(
                    member.profile, 2 if self.team.japanese_mode else 1
                ),
            )
        table.render()

team_building = TeamBuilding()
team_building.run(planning_prompt)
