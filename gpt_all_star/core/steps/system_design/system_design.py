from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.system_design.additional_tasks import additional_tasks
from gpt_all_star.core.steps.system_design import new_functions
from gpt_all_star.core.team import Team


class SystemDesign(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        supervisor = (
            self.agents.copilot.create_assign_supervisor_chain(
                members=self.agents.members()
            )
            .invoke({"messages": [Message.create_human_message("")]})
            .get("assign")
        )
        self.agents.copilot.state(f"Supervisor assignment: {supervisor}.")

        team = Team(
            supervisor=self.agents.get_agent_by_name(supervisor),
            members=self.agents.members(),
        )

        team.drive(None, additional_tasks)
        team.supervisor.output_md(team.storages().docs.get("technologies.md", ""))
        team.supervisor.output_md(team.storages().docs.get("files.md", ""))
