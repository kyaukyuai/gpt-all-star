from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.execution import Execution
from gpt_all_star.core.steps.step import Step


class Improvement(Step):
    def __init__(
        self, agents: Agents, japanese_mode: bool, auto_mode: bool, debug_mode: bool
    ) -> None:
        super().__init__(agents, japanese_mode, auto_mode, debug_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the improvement step!")
        self.console.new_lines(1)
        self.agents.engineer.improve_source_code(auto_mode=self.auto_mode)

        response = self.agents.copilot.ask(
            "Do you want to check the execution again?(y/n)"
        )
        if response.lower() in ["y", "yes"]:
            Execution(
                self.agents, self.japanese_mode, self.auto_mode, self.debug_mode
            ).run()
