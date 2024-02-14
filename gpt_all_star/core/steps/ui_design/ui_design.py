from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.planning_prompt import planning_prompt_template
from gpt_all_star.core.team import Team


class UIDesign(Step):
    '''This class represents the UI Design step in the project workflow.

    The UIDesign step involves creating a detailed and specific development plan to enhance the UI and UX in accordance with human interface guidelines.

    Attributes:
        agents (Agents): The agents involved in the project.
        japanese_mode (bool): Flag indicating whether the project is in Japanese mode.
        review_mode (bool): Flag indicating whether the project is in review mode.
        debug_mode (bool): Flag indicating whether the project is in debug mode.
    '''
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
            current_source_code=team.supervisor.current_source_code(),
            specifications=team.supervisor.storages.docs["specifications.md"],
        )

        team.drive(planning_prompt)
