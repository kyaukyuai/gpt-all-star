from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class Execution(Step):
    def __init__(self, agents: Agents, japanese_mode: bool, auto_mode: bool) -> None:
        super().__init__(agents, japanese_mode, auto_mode)

    def run(self) -> None:
        from gpt_all_star.core.steps.improvement import Improvement

        self.agents.copilot.state("Let's move on to the execution step!")
        self.console.new_lines(1)
        self.agents.copilot.execute_code()

        response = self.agents.copilot.ask(
            "Do you want to improve your source code again?(y/n)"
        )
        if response.lower() in ["y", "yes"]:
            Improvement(self.agents, self.japanese_mode).run()
