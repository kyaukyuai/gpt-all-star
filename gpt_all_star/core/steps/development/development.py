from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.development.additional_tasks import additional_tasks
from gpt_all_star.core.steps.development.nodejs_tasks import nodejs_tasks
from gpt_all_star.core.steps.development.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step


class Development(Step):
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
            specifications=self.agents.copilot.storages.docs.get(
                "specifications.md", "N/A"
            ),
            technologies=self.agents.copilot.storages.docs.get(
                "technologies.md", "N/A"
            ),
            files=self.agents.copilot.storages.docs.get("files.md", "N/A"),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return additional_tasks + nodejs_tasks
