from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.improvement.planning_prompt import planning_prompt_template
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

    def planning_prompt(self) -> str:
        request = self.agents.engineer.ask(
            "What would you like to update?", is_required=True, default=None
        )

        planning_prompt = planning_prompt_template.format(
            request=request,
            current_source_code=self.agents.copilot.current_source_code(),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []
