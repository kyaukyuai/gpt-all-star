from gpt_all_star.cli.console_terminal import MAIN_COLOR
from gpt_all_star.core.agents.agent import AgentRole
from gpt_all_star.helper.text_parser import TextParser
from rich.table import Table


class TeamTable:
    def display_team_members(self, team_members):
        table = Table(show_header=True, header_style=f"{MAIN_COLOR}", title="Team Members")
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Profile")

        for member in team_members:
            table.add_row(
                member.name,
                member.role.name,
                TextParser.cut_last_n_lines(member.profile, 2)
            )

        console.print(table)
