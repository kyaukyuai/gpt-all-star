from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.planning_prompt import planning_prompt_template
from gpt_all_star.core.team import Team


class UIDesign(Step):
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
            current_source_code=team.current_source_code(),
            specifications=team.storages.docs["specifications.md"],
        )

        team.drive(planning_prompt)
