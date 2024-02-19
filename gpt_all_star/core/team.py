import functools
import json
from typing import Optional

from langchain.agents.agent import AgentExecutor
from langgraph.graph import END, StateGraph
from langgraph.pregel import GraphRecursionError

from gpt_all_star.core.agents.agent import ACTIONS, Agent
from gpt_all_star.core.agents.agent_state import AgentState
from gpt_all_star.core.implement_prompt import implement_template
from gpt_all_star.core.message import Message


class Team:
    def __init__(self, supervisor: Agent, members: list[Agent]):
        self.supervisor = supervisor
        self.members = members
        self.supervisor_chain = self._create_supervisor_chain()
        self.state_graph = self._initialize_state_graph()
        self._team = self.state_graph.compile()

    def _create_supervisor_chain(self):
        return self.supervisor.create_supervisor_chain(members=self.members)

    def _initialize_state_graph(self):
        state_graph = StateGraph(AgentState)
        for member in self.members:
            self._add_node_to_graph(member, state_graph)
        self._add_entry_point_to_graph(state_graph)
        self._add_edges_to_graph(state_graph)
        return state_graph

    def _add_node_to_graph(self, agent: Agent, state_graph):
        state_graph.add_node(
            agent.name,
            functools.partial(self._agent_node, agent=agent.executor, name=agent.name),
        )

    def _add_edges_to_graph(self, state_graph):
        for member in self.members:
            state_graph.add_edge(member.name, "supervisor")

    def _add_entry_point_to_graph(self, state_graph):
        state_graph.add_node("supervisor", self.supervisor_chain)
        member_names = [member.name for member in self.members]
        conditional_map = {k: k for k in member_names}
        conditional_map["FINISH"] = END
        state_graph.add_conditional_edges(
            "supervisor", lambda x: x["next"], conditional_map
        )
        state_graph.set_entry_point("supervisor")

    def current_source_code(self):
        return self.supervisor.current_source_code()

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
        self.supervisor.state("Planning tasks in progress")
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
                    implementation=self.current_source_code(),
                    specifications=self.storages().docs.get("specifications.md", "N/A"),
                    technologies=self.storages().docs.get("technologies.md", "N/A"),
                    files=self.storages().docs.get("files.md", "N/A"),
                )
            )
            self.run([message])

    @staticmethod
    def _agent_node(state, agent: AgentExecutor, name):
        result = agent.invoke(state)
        return {"messages": [Message.create_human_message(result["output"], name=name)]}
