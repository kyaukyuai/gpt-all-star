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
            supervisor=self.agents.project_manager,
            members=[
                self.agents.engineer,
                self.agents.designer,
                self.agents.qa_engineer,
            ],
        )

        planning_prompt = planning_prompt_template.format(
            specifications=team.storages().docs["specifications.md"],
            technologies=team.storages().docs["technologies.md"],
            pages=team.storages().docs["pages.md"],
            files=team.storages().docs["files.md"],
        )

        team.drive(planning_prompt, additional_tasks + nodejs_tasks)
