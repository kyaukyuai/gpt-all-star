import json
from typing import Optional

from langgraph.pregel import GraphRecursionError
from rich.status import Status
from rich.table import Table

from gpt_all_star.cli.console_terminal import MAIN_COLOR
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.chain import ACTIONS, Chain
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.development.replanning_prompt import replanning_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.helper.config_loader import load_configuration
from gpt_all_star.helper.multi_agent_collaboration_graph import (
    SUPERVISOR_NAME,
    MultiAgentCollaborationGraph,
)
from gpt_all_star.helper.text_parser import TextParser
from gpt_all_star.helper.translator import create_translator


class Team:
    def __init__(
        self,
        copilot: Copilot,
        members: Agents,
        japanese_mode: bool = False,
        plan_and_solve: bool = False,
    ):
        self.japanese_mode = japanese_mode
        self.plan_and_solve = plan_and_solve
        self.agents = members
        self.copilot = copilot
        self.console = self.copilot.console.console
        self._graph: Optional[MultiAgentCollaborationGraph] = None
        self.supervisor = None
        self._ = create_translator("ja" if japanese_mode else "en")
        self._initialize_team()

    def _initialize_team(self):
        self.copilot.state(self._("Let's start by building a team!"))
        self._introduce_agents()
        self.copilot.state(self._("Ok, we have a team now!"))
        self._display_team_members()

    def _assign_supervisor(self, assign_prompt: str | None):
        supervisor_name = (
            Chain()
            .create_assign_supervisor_chain(members=self.agents.to_array())
            .invoke({"messages": [Message.create_human_message(assign_prompt)]})
            .get("assign")
        )
        supervisor = self.agents.get_agent_by_role(supervisor_name)
        self.copilot.state(self._("Supervisor assignment: %s.") % supervisor.name)
        self._graph = MultiAgentCollaborationGraph(supervisor, self.agents.to_array())
        self.supervisor = supervisor

    def _execute(self, messages: list[Message]):
        try:
            for output in self._graph.workflow.stream(
                {"messages": messages},
                config={"recursion_limit": 50},
            ):
                for key, value in output.items():
                    if key == SUPERVISOR_NAME or key == "__end__":
                        if self.supervisor.debug_mode:
                            self.supervisor.state(value)
                    else:
                        self.agents.get_agent_by_role(key).state(
                            self._("  ┗ I am in charge of it.")
                        )
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

    def _run(self, step: Step):
        assign_prompt = step.assign_prompt()
        planning_prompt = step.planning_prompt()
        additional_tasks = step.additional_tasks()
        step_plan_and_solve = step.plan_and_solve

        self.agents.set_executors(step.working_directory)
        self._assign_supervisor(assign_prompt)

        with Status(
            "[bold white]running...(Have a cup of coffee and relax.)[/bold white]",
            console=self.console,
            spinner="runner",
            speed=0.5,
        ):
            self.supervisor.state(self._("Planning tasks."))
            tasks = (
                Chain()
                .create_planning_chain(self.supervisor.profile)
                .invoke(
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

            MAX_REPLANNING = 10
            replanning = 0
            completed_plan = []
            original_tasks_count = len(tasks["plan"])
            count = 1
            while len(tasks["plan"]) > 0:
                task = tasks["plan"][0]
                working_directory = task.get("working_directory", "")
                file_name = task.get("filename", "")
                if task["action"] == ACTIONS[0]:
                    todo = f"{task['action']}: {task['command']} in the directory({working_directory})"
                elif file_name == "the specific file with placeholders":
                    todo = f"{task['action']}: all files that has any placeholders such as 'TODO', 'PlaceHolder', 'will be added here'"
                elif working_directory == "the directory where the target file exists":
                    todo = f"{task['action']}: {file_name}(a directory follows the directory in which the file resides)"
                else:
                    todo = f"{task['action']}: {working_directory}/{file_name}"

                if self.supervisor.debug_mode:
                    self.supervisor.state(
                        self._(
                            """\n
Task: %s
Context: %s
---
"""
                        )
                        % (todo, task["context"])
                    )
                else:
                    self.supervisor.state(f"({count}/{original_tasks_count}) {todo}")

                message = Message.create_human_message(
                    step.implementation_prompt(
                        task=todo,
                        context=task["context"],
                    )
                )
                self._execute([message])
                count += 1
                tasks["plan"].pop(0)

                if (
                    self.plan_and_solve
                    and step_plan_and_solve
                    and replanning < MAX_REPLANNING
                ):
                    completed_plan.append(task)
                    tasks = (
                        Chain()
                        .create_replanning_chain(self.supervisor.profile)
                        .invoke(
                            {
                                "messages": [
                                    Message.create_human_message(
                                        replanning_template.format(
                                            original_plan=tasks,
                                            completed_plan=completed_plan,
                                            implementation=self.copilot.storages.current_source_code(),
                                            specifications=self.copilot.storages.docs.get(
                                                "specifications.md", "N/A"
                                            ),
                                            technologies=self.copilot.storages.docs.get(
                                                "technologies.md", "N/A"
                                            ),
                                            ui_design=self.copilot.storages.docs.get(
                                                "ui_design.html", "N/A"
                                            ),
                                        )
                                    )
                                ],
                            }
                        )
                    )
                    replanning += 1
                    count = 1
                    original_tasks_count = len(tasks["plan"])
                    if self.supervisor.debug_mode:
                        self.supervisor.console.print(
                            json.dumps(tasks, indent=4, ensure_ascii=False)
                        )

    def _improve(self, step: Step, improvement_request: Optional[str] = None) -> None:
        step.improvement_request = improvement_request
        improvement_prompt = step.improvement_prompt()

        if improvement_prompt == "":
            return None

        self.agents.set_executors(step.working_directory)
        self._assign_supervisor(improvement_prompt)

        with Status(
            "[bold white]running...(Have a cup of coffee and relax.)[/bold white]",
            console=self.console,
            spinner="runner",
            speed=0.5,
        ):
            self.supervisor.state(self._("Planning tasks."))
            tasks = (
                Chain()
                .create_planning_chain(self.supervisor.profile)
                .invoke(
                    {
                        "messages": [Message.create_human_message(improvement_prompt)],
                    }
                )
            )

            if self.supervisor.debug_mode:
                self.supervisor.console.print(
                    json.dumps(tasks, indent=4, ensure_ascii=False)
                )

            original_tasks_count = len(tasks["plan"])
            count = 1
            while len(tasks["plan"]) > 0:
                task = tasks["plan"][0]
                working_directory = task.get("working_directory", "")
                file_name = task.get("filename", "")
                if task["action"] == ACTIONS[0]:
                    todo = f"{task['action']}: {task['command']} in the directory({working_directory})"
                elif file_name == "the specific file with placeholders":
                    todo = f"{task['action']}: all files that has any placeholders such as 'TODO', 'PlaceHolder', 'will be added here'"
                elif working_directory == "the directory where the target file exists":
                    todo = f"{task['action']}: {file_name}(a directory follows the directory in which the file resides)"
                else:
                    todo = f"{task['action']}: {working_directory}/{file_name}"

                if self.supervisor.debug_mode:
                    self.supervisor.state(
                        self._(
                            """\n
Task: %s
Context: %s
---
"""
                        )
                        % (todo, task["context"])
                    )
                else:
                    self.supervisor.state(f"({count}/{original_tasks_count}) {todo}")

                message = Message.create_human_message(
                    step.implementation_prompt(
                        task=todo,
                        context=task["context"],
                    )
                )
                self._execute([message])
                count += 1
                tasks["plan"].pop(0)

    def run(self, step: Step) -> bool:
        self._run(step)

        return step.callback()

    def improve(self, step: Step, improvement_request: Optional[str] = None) -> bool:
        self._improve(step, improvement_request)

        return step.callback()

    def _introduce_agents(self) -> None:
        agents_list = load_configuration("./gpt_all_star/agents.yml")
        if agents_list:
            self.copilot.state(self._("Loading members from `agent.yml`..."))
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
            if role is not AgentRole.COPILOT:
                self._introduce_agent(getattr(self.agents, role.value), role)

    def _introduce_agent(self, agent: Agent, role: AgentRole) -> None:
        self.copilot.state(self._("Please introduce the %s.") % role.name)
        self._ask_agent_name(agent, role)
        self._ask_agent_profile(agent, role)
        self._add_instructions_to_profile(agent)
        agent.messages = [Message.create_system_message(agent.profile)]

    def _ask_agent_name(self, agent: Agent, role: AgentRole) -> None:
        agent.name = self.copilot.ask(
            self._("What is the name of the %s?") % role.name,
            is_required=False,
            default=agent.name,
        )

    def _ask_agent_profile(self, agent: Agent, role: AgentRole) -> None:
        agent.profile = self.copilot.ask(
            self._("What is the profile of the %s?") % role.name,
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
        team_members = [agent for agent in vars(self.agents).values()]
        for member in team_members:
            table.add_row(
                member.name,
                member.role.name,
                TextParser.cut_last_n_lines(
                    member.profile, 2 if self.japanese_mode else 1
                ),
            )
        self.console.print(table)
