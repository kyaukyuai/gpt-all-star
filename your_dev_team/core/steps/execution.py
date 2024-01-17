from your_dev_team.core.agents.agents import Agents
from your_dev_team.core.steps.step import Step


class Execution(Step):
    def __init__(self, agents: Agents, japanese_mode) -> None:
        super().__init__(agents, japanese_mode)

    def run(self) -> None:
        from your_dev_team.core.steps.improvement import Improvement

        self.agents.copilot.state("Let's move on to the execution step!")
        self.console.new_lines(1)
        self.agents.copilot.execute_code()

        response = self.agents.copilot.ask(
            "Do you want to improve your source code again?(y/n)"
        )
        if response.lower() in ["y", "yes"]:
            Improvement(self.agents, self.japanese_mode).run()
