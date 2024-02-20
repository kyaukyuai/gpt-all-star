from gpt_all_star.core.agents import agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.specification.additional_tasks import (
    create_additional_tasks,
)
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team


class Specification(Step):
    def __init__(
        self,
        agents: agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        instructions = self.agents.product_owner.get_instructions()
        app_type = self.agents.product_owner.get_app_type()
        self.agents.copilot.state("Ok, we have a instruction and app type now!")
        self.agents.copilot.console.print(
            f"""
---
instruction:
{instructions}
app_type:
{app_type}
---
""",
            style="bold",
        )

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

        team.drive(None, create_additional_tasks(app_type, instructions))
        team.supervisor.output_md(team.storages().docs.get("specifications.md", ""))
