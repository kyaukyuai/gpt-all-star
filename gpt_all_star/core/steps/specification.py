from gpt_all_star.core.agents import agents
from gpt_all_star.core.implement_planning_prompt import implement_planning_template
from gpt_all_star.core.message import Message
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

        team = Team(
            supervisor=self.agents.project_manager,
            members=[
                self.agents.product_owner,
                self.agents.designer,
                self.agents.engineer,
            ],
        )
        todo_list = {
            "plan": [
                {
                    "task": "Add a new file",
                    "working_directory": "./docs/",
                    "filename": "specifications.md",
                    "command": "",
                    "context": f"""The task is to clarify specifications of a {app_type}.
Your role is to read and understand the instructions and provide the specifications, not to implement them.
Please itemize the list of specifications inferred from the instructions.
**IMPORTANT**: Please keep the specifications as minimal as possible to build our MVP (Minimum Viable Product).
The following are requirements that your application must meet: ```{instructions}```
""",
                    "objective": f"""To document a clear and concise list of specifications for the {app_type}, derived from the given instructions.
This document will serve as the basis for developing a Minimum Viable Product (MVP), ensuring that the development focuses on essential features required for the initial launch.
""",
                    "reason": """Establishing a clear set of specifications for the MVP is crucial to guide the development process efficiently and effectively.
By focusing on minimal requirements, resources can be optimally allocated to deliver a product that meets the core objectives, facilitating quicker iterations and feedback cycles.
This approach helps in validating the product concept with the least amount of effort and investment.
""",
                }
            ]
        }
        for i, task in enumerate(todo_list["plan"]):
            if task["task"] == "Execute a command":
                todo = f"{task['task']}: {task['command']} in the directory {task['working_directory']}"
            else:
                todo = f"{task['task']}: {task['working_directory']}/{task['filename']}"

            team.supervisor.state(
                f"""\n
Task {i + 1}: {todo}
Context: {task['context']}
Objective: {task['objective']}
Reason: {task['reason']}
---
"""
            )

            message = Message.create_human_message(
                implement_planning_template.format(
                    task=todo,
                    objective=task["objective"],
                    context=task["context"],
                    reason=task["reason"],
                    implementation=None,
                    specifications=None,
                )
            )
            team.run([message])
