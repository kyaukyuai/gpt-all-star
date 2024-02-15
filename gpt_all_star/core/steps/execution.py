from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.planning_prompt import \
    planning_prompt_template
from gpt_all_star.core.team import Team


class Execution(Step):
    """
    Represents the execution step of the development process.

    This class is responsible for executing the development plan and handling any errors that occur during execution.

    Attributes:
        agents (Agents): The collection of autonomous AI agents involved in the development process.
        japanese_mode (bool): Flag indicating whether the execution is in Japanese mode.
        review_mode (bool): Flag indicating whether the execution is in review mode.
        debug_mode (bool): Flag indicating whether the execution is in debug mode.
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
        Executes the development plan.

        This method runs the command specified by the QA engineer and handles any exceptions that occur during execution.
        If an exception occurs, it notifies the team and provides the error details and the current source code.

        Raises:
            KeyboardInterrupt: If the execution is interrupted by the user.
            Exception: If any other exception occurs during execution.
        """
        """
        Executes the development plan.

        This method runs the command specified by the QA engineer and handles any exceptions that occur during execution.
        If an exception occurs, it notifies the team and provides the error details and the current source code.

        Raises:
            KeyboardInterrupt: If the execution is interrupted by the user.
            Exception: If any other exception occurs during execution.
        """
        from gpt_all_star.core.steps.improvement import Improvement

        self.agents.qa_engineer.confirm_execution(
            review_mode=self.review_mode,
            command=self.agents.qa_engineer.storages.root["run.sh"],
        )
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.agents.qa_engineer.state(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}")
            try:
                self.agents.qa_engineer.run_command()
            except KeyboardInterrupt:
                break
            except Exception as e:
                team = Team(
                    supervisor=self.agents.project_manager,
                    members=[
                        self.agents.engineer,
                        self.agents.designer,
                        self.agents.qa_engineer,
                    ],
                )
                team.drive(
                    planning_prompt_template.format(
                        error=e,
                        current_source_code=team.supervisor.current_source_code(),
                    )
                )

        CONFIRM_CHOICES = ["yes", "no"]
        choice = self.agents.copilot.present_choices(
            "Do you want to improve your source code again?",
            CONFIRM_CHOICES,
            default=1,
        )
        if choice == CONFIRM_CHOICES[0]:
            Improvement(
                self.agents, self.japanese_mode, self.review_mode, self.debug_mode
            )
