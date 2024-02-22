import json
from typing import Optional

from langgraph.pregel import GraphRecursionError
from rich.status import Status
from rich.table import Table

from gpt_all_star.cli.console_terminal import MAIN_COLOR, ConsoleTerminal
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.chain import (
    ACTIONS,
    create_assign_supervisor_chain,
    create_planning_chain,
)
from gpt_all_star.core.implement_prompt import implement_template
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.helper.config_loader import load_configuration
from gpt_all_star.helper.multi_agent_collaboration_graph import (
    SUPERVISOR_NAME,
    MultiAgentCollaborationGraph,
)
from gpt_all_star.helper.text_parser import TextParser


class Team:
    def __init__(self, members: Agents, japanese_mode: bool = False):
        self.japanese_mode = japanese_mode
        self.console = ConsoleTerminal()
        self.agents = members
        self.members = members.members()
        self._graph: Optional[MultiAgentCollaborationGraph] = None
        self.agents.copilot.state("Let's start by building a team!")
        self.console.new_lines()
        self._introduce_agents()
        self.console.new_lines()
        self.agents.copilot.state("Ok, we have a team now!")
        self._display_team_members()

    def _assign_supervisor(self, planning_prompt: str | None):
        supervisor = (
            create_assign_supervisor_chain(members=self.members)
            .invoke({"messages": [Message.create_human_message(planning_prompt)]})
            .get("assign")
        )
        print(f"Supervisor assignment: {supervisor}.")
        self._graph = MultiAgentCollaborationGraph(
            self.agents.get_agent_by_name(supervisor), self.members
        )

    def storages(self):
        return self._graph.supervisor.storages

    def _run(self, messages: list[Message]):
    def _execute_task(self, task):
        if task["action"] == ACTIONS[0]:
            todo = f"{task['action']}: {task['command']} in the directory({task.get('working_directory', '')})"
        else:
            todo = f"{task['action']}: {task.get('working_directory', '')}/{task.get('filename', '')}"

        if self._graph.supervisor.debug_mode:
            self._graph.supervisor.state(
                f"""\n
Task {i + 1}: {todo}
Context: {task['context']}
Objective: {task['objective']}
Reason: {task['reason']}
---
"""
            )
        else:
            self._graph.supervisor.state(
                f"({(i+1)}/{len(tasks['plan'])}) {todo}"
            )

        message = Message.create_human_message(
            implement_template.format(
                task=todo,
                objective=task["objective"],
                context=task["context"],
                reason=task["reason"],
                implementation=self._graph.supervisor.current_source_code(),
                specifications=self.storages().docs.get(
                    "specifications.md", "N/A"
                ),
                technologies=self.storages().docs.get("technologies.md", "N/A"),
                files=self.storages().docs.get("files.md", "N/A"),
            )
        )
        self._run([message])

    def _execute_tasks(self, tasks):
        for i, task in enumerate(tasks["plan"]):
            self._execute_task(task)

    def drive(
        self,
        planning_prompt: Optional[str] = None,
        additional_tasks: list = [],
    ):
        with Status(
            "[bold green]running...",
            console=self.agents.copilot.console.console,
            spinner="runner",
            speed=0.5,
        ):
            self._graph.supervisor.state("Planning tasks.")
            tasks = (
                create_planning_chain(self._graph.supervisor.profile).invoke(
                    {
                        "messages": [Message.create_human_message(planning_prompt)],
                    }
                )
                if planning_prompt
                else {"plan": []}
            )
            for task in additional_tasks:
                tasks["plan"].append(task)

            if self._graph.supervisor.debug_mode:
                self._graph.supervisor.console.print(
                    json.dumps(tasks, indent=4, ensure_ascii=False)
                )

            self._execute_tasks(tasks)
                else:
                    todo = f"{task['action']}: {task.get('working_directory', '')}/{task.get('filename', '')}"

                if self._graph.supervisor.debug_mode:
                    self._graph.supervisor.state(
                        f"""\n
Task {i + 1}: {todo}
Context: {task['context']}
Objective: {task['objective']}
Reason: {task['reason']}
---
"""
                    )
                else:
                    self._graph.supervisor.state(
                        f"({(i+1)}/{len(tasks['plan'])}) {todo}"
                    )

                message = Message.create_human_message(
                    implement_template.format(
                        task=todo,
                        objective=task["objective"],
                        context=task["context"],
                        reason=task["reason"],
                        implementation=self._graph.supervisor.current_source_code(),
                        specifications=self.storages().docs.get(
                            "specifications.md", "N/A"
                        ),
                        technologies=self.storages().docs.get("technologies.md", "N/A"),
                        files=self.storages().docs.get("files.md", "N/A"),
                    )
                )
                self._run([message])

    def run(self, step: Step):
        planning_prompt = step.planning_prompt()
        additional_tasks = step.additional_tasks()
        self._assign_supervisor(planning_prompt)
        self.drive(planning_prompt, additional_tasks)

    def _introduce_agents(self) -> None:
        agents_list = load_configuration("./gpt_all_star/agents.yml")
        if agents_list:
            for agent_info in agents_list:
                self._set_agent_attributes(agent_info)
        else:
            self._introduce_agents_manually()

    def _set_agent_attributes(self, agent_info: dict) -> None:
        agent = getattr(self.agents, agent_info["role"])
        agent.name = agent_info["name"]
        agent.profile = agent_info["profile"]
        self._add_instructions_to_profile(agent)
        agent.messages = [Message.create_system_message(agent.profile)]

    def _add_instructions_to_profile(self, agent: Agent) -> None:
        agent.profile += "\nAny instruction you get that is labeled as **IMPORTANT**, you follow strictly."
        if self.japanese_mode:
            agent.profile += "\n**IMPORTANT: 必ず日本語で書いて下さい**"

    def _introduce_agents_manually(self) -> None:
        for role in AgentRole:
            if role != AgentRole.COPILOT:
                self._introduce_agent(getattr(self.agents, role.value), role)

    def _introduce_agent(self, agent: Agent, role: AgentRole) -> None:
        self.agents.copilot.state(f"Please introduce the {role.name}.")
        self._ask_agent_name(agent, role)
        self._ask_agent_profile(agent, role)
        self._add_instructions_to_profile(agent)
        agent.messages = [Message.create_system_message(agent.profile)]

    def _ask_agent_name(self, agent: Agent, role: AgentRole) -> None:
        agent.name = self.agents.copilot.ask(
            f"What is the name of the {role.name}?",
            is_required=False,
            default=agent.name,
        )

    def _ask_agent_profile(self, agent: Agent, role: AgentRole) -> None:
        agent.profile = self.agents.copilot.ask(
            f"What is the profile of the {role.name}?",
            is_required=False,
            default=agent.profile,
        )

    def _display_team_members(self) -> None:
        table = Table(
            show_header=True, header_style=f"{MAIN_COLOR}", title="Team Members"
        )
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Profile")
        team_members = [
            agent
            for agent in vars(self.agents).values()
            if agent.role != AgentRole.COPILOT
        ]
        for member in team_members:
            table.add_row(
                member.name,
                member.role.name,
                TextParser.cut_last_n_lines(
                    member.profile, 2 if self.japanese_mode else 1
                ),
            )
        self.console.print(table)
        self.console.new_lines(1)
