from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class Development(Step):
    def __init__(self, agents: Agents, japanese_mode: bool, auto_mode: bool) -> None:
        super().__init__(agents, japanese_mode, auto_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the development step!")
        self.console.new_lines()
        # self.agents.engineer.create_source_code(auto_mode=self.auto_mode)
        # self.agents.designer.design_user_interface(auto_mode=self.auto_mode)
        # self.console.new_lines()
        self.agents.qa_engineer.evaluate_source_code(auto_mode=self.auto_mode)
        self.console.new_lines()
