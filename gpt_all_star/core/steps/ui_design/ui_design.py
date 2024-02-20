from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.ui_design.planning_prompt import planning_prompt_template
from gpt_all_star.core.team import Team


class UIDesign(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        planning_prompt = self._create_planning_prompt()(
            current_source_code=self.agents.copilot.current_source_code(),
            specifications=self.agents.copilot.storages.docs.get(
                "specifications.md", "N/A"
            ),
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

        team.drive(planning_prompt)
