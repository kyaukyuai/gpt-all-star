from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import additional_tasks
from gpt_all_star.core.team import Team


class SystemDesign(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        team = Team(supervisor=self.agents.architect, members=self.agents.members())

        team.drive(None, additional_tasks)
        team.supervisor.output_md(team.storages().docs.get("technologies.md", ""))
        team.supervisor.output_md(team.storages().docs.get("files.md", ""))
