from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.execution import Execution
from gpt_all_star.core.steps.step import Step


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
        self.agents.engineer.improve_source_code(review_mode=self.review_mode)

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
