from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.development.additional_tasks import additional_tasks
from gpt_all_star.core.steps.development.nodejs_tasks import nodejs_tasks
from gpt_all_star.core.steps.development.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class Development(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        team = Team(
            supervisor=self.agents.project_manager, members=self.agents.members()
        )

        planning_prompt = planning_prompt_template.format(
            specifications=team.storages().docs.get("specifications.md", None),
            technologies=team.storages().docs.get("technologies.md", None),
            pages=team.storages().docs.get("pages.md", None),
            files=team.storages().docs.get("files.md", None),
        )

        team.drive(planning_prompt, additional_tasks + nodejs_tasks)
