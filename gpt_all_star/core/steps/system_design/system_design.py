from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import additional_tasks


class SystemDesign(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def planning_prompt(self) -> str:
        return ""

    def additional_tasks(self) -> list:
        return additional_tasks
