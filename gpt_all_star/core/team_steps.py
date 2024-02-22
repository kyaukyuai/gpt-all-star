import json
from typing import Optional

from gpt_all_star.cli.console_terminal import MAIN_COLOR
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.chain import (ACTIONS,
                                            create_assign_supervisor_chain,
                                            create_planning_chain)
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.implement_prompt import implement_template
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.team import GraphRecursionError, Team
from gpt_all_star.helper.config_loader import load_configuration
from gpt_all_star.helper.multi_agent_collaboration_graph import (
    SUPERVISOR_NAME, MultiAgentCollaborationGraph)
from gpt_all_star.helper.text_parser import TextParser
from rich.status import Status
from rich.table import Table


def assign_supervisor(planning_prompt: str | None):
    supervisor_name = (
        create_assign_supervisor_chain(members=Agents.to_array())
        .invoke({"messages": [Message.create_human_message(planning_prompt)]})
        .get("assign")
    )
    Copilot.state(f"Supervisor assignment: {supervisor_name}.")
    supervisor = Agents.get_agent_by_name(supervisor_name)
    Team._graph = MultiAgentCollaborationGraph(supervisor, Agents.to_array())
    Team.supervisor = supervisor


def execute(messages: list[Message]):
    try:
        for output in Team._graph.workflow.stream(
            {"messages": messages},
            config={"recursion_limit": 10},
        ):
            for key, value in output.items():
                if key == SUPERVISOR_NAME or key == "__end__":
                    if Team.supervisor.debug_mode:
                        Team.supervisor.state(value)
                else:
                    Agents.get_agent_by_name(key).state("  ┗ I am in charge of it.")
                    if Team.supervisor.debug_mode:
                        latest_message = value.get("messages")[-1].content.strip()
                        Team.supervisor.console.print(
                            f"""
{key}:
---
{latest_message}
---
"""
                        )
    except GraphRecursionError:
        if Team.supervisor.debug_mode:
            print("Recursion limit reached")


def run_task(planning_prompt: Optional[str] = None, additional_tasks: list = []):
    with Status(
        "[bold green]running...",
        console=Copilot.console,
        spinner="runner",
        speed=0.5,
    ):
        if not Team._graph:
            assign_supervisor(planning_prompt)

        Team.supervisor.state("Planning tasks.")
        tasks = (
            create_planning_chain(Team.supervisor.profile).invoke(
                {"messages": [Message.create_human_message(planning_prompt)]}
            )
            if planning_prompt
            else {"plan": []}
        )
        for task in additional_tasks:
            tasks["plan"].append(task)

        if Team.supervisor.debug_mode:
            Team.supervisor.console.print(
                json.dumps(tasks, indent=4, ensure_ascii=False)
            )

        for i, task in enumerate(tasks["plan"]):
            if task["action"] == ACTIONS[0]:
                todo = f"{task['action']}: {task['command']} in the directory({task.get('working_directory', '')})"
            else:
                todo = f"{task['action']}: {task.get('working_directory', '')}/{task.get('filename', '')}"

            if Team.supervisor.debug_mode:
                Team.supervisor.state(
                    f"""\n
Task {i + 1}: {todo}
Context: {task['context']}
Objective: {task['objective']}
Reason: {task['reason']}
---
"""
                )
            else:
                Team.supervisor.state(f"({(i+1)}/{len(tasks['plan'])}) {todo}")

            message = Message.create_human_message(
                implement_template.format(
                    task=todo,
                    objective=task["objective"],
                    context=task["context"],
                    reason=task["reason"],
                    implementation=Storages.current_source_code(),
                    specifications=Storages.docs.get("specifications.md", "N/A"),
                    technologies=Storages.docs.get("technologies.md", "N/A"),
                    files=Storages.docs.get("files.md", "N/A"),
                )
            )
            execute([message])


def introduce_agents() -> None:
    agents_list = load_configuration("./gpt_all_star/agents.yml")
    if agents_list:
        Copilot.state("Loading members from `agent.yml`...")
        for agent_info in agents_list:
            set_agent_attributes(agent_info)
    else:
        introduce_agents_manually()


def set_agent_attributes(agent_info: dict) -> None:
    agent = getattr(Agents, agent_info["role"])
    agent.name = agent_info["name"]
    agent.profile = agent_info["profile"]
    add_instructions_to_profile(agent)
    agent.messages = [Message.create_system_message(agent.profile)]


def add_instructions_to_profile(agent: Agent) -> None:
    agent.profile += "\nAny instruction you get that is labeled as **IMPORTANT**, you follow strictly."
    if Team.japanese_mode:
        agent.profile += "\n**IMPORTANT: 必ず日本語で書いて下さい**"


def introduce_agents_manually() -> None:
    for role in AgentRole:
        introduce_agent(getattr(Agents, role.value), role)


def introduce_agent(agent: Agent, role: AgentRole) -> None:
    Copilot.state(f"Please introduce the {role.name}.")
    ask_agent_name(agent, role)
    ask_agent_profile(agent, role)
    add_instructions_to_profile(agent)
    agent.messages = [Message.create_system_message(agent.profile)]


def ask_agent_name(agent: Agent, role: AgentRole) -> None:
    agent.name = Copilot.ask(
        f"What is the name of the {role.name}?",
        is_required=False,
        default=agent.name,
    )


def ask_agent_profile(agent: Agent, role: AgentRole) -> None:
    agent.profile = Copilot.ask(
        f"What is the profile of the {role.name}?",
        is_required=False,
        default=agent.profile,
    )


def display_team_members() -> None:
    table = Table(
        show_header=True, header_style=f"{MAIN_COLOR}", title="Team Members"
    )
    table.add_column("Name")
    table.add_column("Role")
    table.add_column("Profile")
    team_members = [agent for agent in vars(Agents).values()]
    for member in team_members:
        table.add_row(
            member.name,
            member.role.name,
            TextParser.cut_last_n_lines(
                member.profile, 2 if Team.japanese_mode else 1
            ),
        )
    Copilot.console.print(table)
