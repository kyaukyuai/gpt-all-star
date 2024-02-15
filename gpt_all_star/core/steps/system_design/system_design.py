from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design import additional_tasks
from gpt_all_star.core.team import Team


class SystemDesign(Step):
    """A class representing the system design step in the project."""
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        """Initialize the SystemDesign class.

        Args:
            agents: An instance of the Agents class.
            japanese_mode: A boolean indicating whether Japanese mode is enabled.
            review_mode: A boolean indicating whether review mode is enabled.
            debug_mode: A boolean indicating whether debug mode is enabled.
        """
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        """Run the system design step."""
        team = Team(
            supervisor=self.agents.project_manager,
            members=[
                self.agents.architect,
                self.agents.designer,
                self.agents.engineer,
            ],
        )

        team.drive(None, additional_tasks)
