from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class Execution(Step):
    def __init__(self, agents: Agents, japanese_mode: bool, auto_mode: bool) -> None:
        super().__init__(agents, japanese_mode, auto_mode)

    def run(self) -> None:
        from gpt_all_star.core.steps.improvement import Improvement

        self.agents.copilot.state("Let's move on to the execution step!")
        self.console.new_lines()
        self.agents.copilot.execute_code(auto_mode=self.auto_mode)

        CONFIRM_CHOICES = ["yes", "no"]
        choice = self.agents.copilot.present_choices(
            "Do you want to improve your source code again?",
            CONFIRM_CHOICES,
            default=1,
        )
        if choice == CONFIRM_CHOICES[0]:
            Improvement(self.agents, self.japanese_mode, self.auto_mode).run()
