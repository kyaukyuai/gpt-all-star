from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.execution import Execution
from gpt_all_star.core.steps.improvement.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class Improvement(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        """Run the Improvement step."""
        team = Team(
            supervisor=self.agents.project_manager,
            members=[
                self.agents.engineer,
                self.agents.designer,
                self.agents.qa_engineer,
            ],
        )

        request = self.agents.engineer.ask(
            "What would you like to update?", is_required=True, default=None
        )

        planning_prompt = planning_prompt_template.format(
            request=request,
            current_source_code=team.supervisor.current_source_code(),
        )
        team.drive(planning_prompt)

        CONFIRM_CHOICES = ["yes", "no"]
        choice = self.agents.copilot.present_choices(
            "Do you want to check the execution again?",
            CONFIRM_CHOICES,
            default=1,
        )
        if choice == CONFIRM_CHOICES[0]:
            Execution(
                self.agents, self.japanese_mode, self.review_mode, self.debug_mode
            ).run()
            ).run()
