from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.execution.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class Execution(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        from gpt_all_star.core.steps.improvement.improvement import Improvement

        self.agents.qa_engineer.confirm_execution(
            review_mode=self.review_mode,
            command=self.agents.qa_engineer.storages.root["./app/run.sh"],
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
                    supervisor=self.agents.qa_engineer,
                    members=self.agents.members(),
                )
                team.drive(
                    planning_prompt_template.format(
                        error=e,
                        current_source_code=team.current_source_code(),
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
            ).run()
