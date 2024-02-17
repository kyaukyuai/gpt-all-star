from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import additional_tasks
from gpt_all_star.core.team import Team


class SystemDesign(Step):
    """
    This class represents the system design step.

    Args:
        agents (Agents): The agents involved in the system design.
        japanese_mode (bool): Whether the system design is in Japanese mode.
        review_mode (bool): Whether the system design is in review mode.
        debug_mode (bool): Whether the system design is in debug mode.
    """
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        """
        This method runs the system design step.

        Returns:
            None
        """
        team = Team(supervisor=self.agents.architect, members=self.agents.members())

        team.drive(None, additional_tasks)
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        team = Team(supervisor=self.agents.architect, members=self.agents.members())

        team.drive(None, additional_tasks)
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        """
        This method runs the system design step.

        Returns:
            None
        """
        team = Team(supervisor=self.agents.architect, members=self.agents.members())

        team.drive(None, additional_tasks)
