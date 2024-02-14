# gpt_all_star/core/steps/improvement/team.py

from gpt_all_star.core.steps.step import Agent
from gpt_all_star.core.steps.team_building import ProjectManager


class Team:
    def __init__(self, supervisor: Agent, members: list[Agent]) -> None:
        self.supervisor = supervisor
        self.members = members

    def current_source_code(self) -> str:
        return self.supervisor.current_source_code()
