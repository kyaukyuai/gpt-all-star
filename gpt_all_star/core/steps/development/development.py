from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.development.additional_tasks import additional_tasks
from gpt_all_star.core.steps.development.nodejs_tasks import nodejs_tasks
from gpt_all_star.core.steps.development.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class Development(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        planning_prompt = planning_prompt_template.format(
            specifications=self.agents.copilot.storages.docs.get(
                "specifications.md", "N/A"
            ),
            technologies=self.agents.copilot.storages.docs.get(
                "technologies.md", "N/A"
            ),
            files=self.agents.copilot.storages.docs.get("files.md", "N/A"),
        )

        supervisor = (
            self.agents.copilot.create_assign_supervisor_chain(
                members=self.agents.members()
            )
            .invoke({"messages": [Message.create_human_message(planning_prompt)]})
            .get("assign")
        )
        self.agents.copilot.state(f"Supervisor assignment: {supervisor}.")

        team = Team(
            supervisor=self.agents.get_agent_by_name(supervisor),
            members=self.agents.members(),
        )

        team.drive(planning_prompt, additional_tasks + nodejs_tasks)
