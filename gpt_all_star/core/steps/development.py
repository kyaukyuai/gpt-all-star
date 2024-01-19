from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class Development(Step):
    def __init__(self, agents: Agents, japanese_mode) -> None:
        super().__init__(agents, japanese_mode)

    def run(self) -> None:
        self.agents.copilot.state("Let's move on to the development step!")
        self.console.new_lines(1)
        self.agents.engineer.state("How about the following?")
        self.agents.engineer.generate_source_code()
        self.agents.designer.arrange_ui_design()
        self.agents.engineer.generate_entrypoint()
        self.agents.engineer.generate_readme()
        self.console.new_lines(1)
