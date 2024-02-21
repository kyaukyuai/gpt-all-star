import json
from typing import Optional

from langgraph.pregel import GraphRecursionError

from gpt_all_star.core.agents.agent import ACTIONS, Agent
from gpt_all_star.core.implement_prompt import implement_template
from gpt_all_star.core.message import Message
from gpt_all_star.helper.multi_agent_collaboration_graph import (
    MultiAgentCollaborationGraph,
)


class Team:
    """
    Represents a team of agents and provides methods for managing the team's activities.

    Attributes:
        supervisor (Agent): The supervisor agent.
        members (list[Agent]): List of member agents.
    """ # Updated docstring
    def __init__(self, supervisor: Agent, members: list[Agent]):
        self.supervisor = supervisor
        self.members = members
        self._team = MultiAgentCollaborationGraph(
            self.supervisor, self.members
        ).workflow

    def storages(self):
        return self.supervisor.storages

    def run(self, messages: list[Message]):
        try:
            for output in self._team.stream(
                {"messages": messages},
                config={"recursion_limit": 10},
            ):
                for key, value in output.items():
                    if key == "supervisor" or key == "__end__":
                        if self.supervisor.debug_mode:
                            self.supervisor.state(value)
                    else:
                        self.supervisor.console.print(f"  ┗ {key} is in charge of it.")
                        if self.supervisor.debug_mode:
                            latest_message = value.get("messages")[-1].content.strip()
                            self.supervisor.console.print(
                                f"""
{key}:
---
{latest_message}
---
"""
                            )
        except GraphRecursionError:
            if self.supervisor.debug_mode:
                print("Recursion limit reached")

    def drive(
        self,
        planning_prompt: Optional[str] = None,
        additional_tasks: list[str] = [],
    ):
        self.supervisor.state("Planning tasks.")
        tasks = (
            self.supervisor.create_planning_chain().invoke(
                {
                    "messages": [Message.create_human_message(planning_prompt)],
                }
            )
            if planning_prompt
            else {"plan": []}
        )
        for task in additional_tasks:
            tasks["plan"].append(task)

        if self.supervisor.debug_mode:
            self.supervisor.console.print(
                json.dumps(tasks, indent=4, ensure_ascii=False)
            )

        for i, task in enumerate(tasks["plan"]):
            if task["action"] == ACTIONS[0]:
                todo = f"{task['action']}: {task['command']} in the directory({task.get('working_directory', '')})"
            else:
                todo = f"{task['action']}: {task.get('working_directory', '')}/{task.get('filename', '')}"

            if self.supervisor.debug_mode:
                self.supervisor.state(
                    f"""\n
Task {i + 1}: {todo}
Context: {task['context']}
Objective: {task['objective']}
Reason: {task['reason']}
---
"""
                )
            else:
                self.supervisor.state(f"({(i+1)}/{len(tasks['plan'])}) {todo}")

            message = Message.create_human_message(
                implement_template.format(
                    task=todo,
                    objective=task["objective"],
                    context=task["context"],
                    reason=task["reason"],
                    implementation=self.supervisor.current_source_code(),
                    specifications=self.storages().docs.get("specifications.md", "N/A"),
                    technologies=self.storages().docs.get("technologies.md", "N/A"),
                    files=self.storages().docs.get("files.md", "N/A"),
                )
            )
            self.run([message])
