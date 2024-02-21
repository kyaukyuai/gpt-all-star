from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.planning_prompt import planning_prompt_template


class UIDesign(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def planning_prompt(self) -> str:
        planning_prompt = planning_prompt_template.format(
            current_source_code=self.agents.copilot.current_source_code(),
            specifications=self.agents.copilot.storages.docs.get(
                "specifications.md", "N/A"
            ),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []
