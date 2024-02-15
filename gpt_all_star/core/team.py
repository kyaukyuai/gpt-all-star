import functools
import json
from typing import Optional

from langchain.agents.agent import AgentExecutor
from langgraph.graph import END, StateGraph
from langgraph.pregel import GraphRecursionError

from gpt_all_star.core.agents.agent import Agent
from gpt_all_star.core.agents.agent_state import AgentState
from gpt_all_star.core.implement_planning_prompt import implement_planning_template
from gpt_all_star.core.message import Message


class Team:
    def __init__(self, supervisor: Agent, members: list[Agent]):
        self.supervisor = supervisor
        self.members = members
        self.supervisor_chain = self._create_supervisor_chain()
        self.state_graph = self._initialize_state_graph()
        self._team = self.state_graph.compile()

    def _create_supervisor_chain(self):
        return self.supervisor.create_supervisor_chain(
            members=[member.name for member in self.members]
        )

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
            state_graph.add_edge(member.name, self.supervisor.name)

    def _add_entry_point_to_graph(self, state_graph):
        state_graph.add_node(self.supervisor.name, self.supervisor_chain)
        member_names = [member.name for member in self.members]
        conditional_map = {k: k for k in member_names}
        conditional_map["FINISH"] = END
        state_graph.add_conditional_edges(
            self.supervisor.name, lambda x: x["next"], conditional_map
        )
        state_graph.set_entry_point(self.supervisor.name)

    def current_source_code(self):
        return self.supervisor.current_source_code()

    def storages(self):
        return self.supervisor.storages

    def run(self, messages: list[Message]):
        try:
            for output in self._team.stream(
                {"messages": messages},
                config={"recursion_limit": 25},
            ):
                for key, value in output.items():
                    if key == self.supervisor.name or key == "__end__":
                        # self.supervisor.state(value)
                        pass
                    else:
                        latest_message = value.get("messages")[-1].content.strip()
                        self.supervisor.console.print(
                            f"""
    {key}:
    ---
    {latest_message}
    ---\n
    """
                        )
        except GraphRecursionError:
            print("Recursion limit reached")

    def drive(
        self, planning_prompt: Optional[str] = None, additional_tasks: list[str] = []
    ):
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
        self.supervisor.console.print(json.dumps(tasks, indent=4, ensure_ascii=False))

        for i, task in enumerate(tasks["plan"]):
            if task["task"] == "Execute a command":
                todo = f"{task['task']}: {task['command']} in the directory {task['working_directory']}"
            else:
                todo = f"{task['task']}: {task['working_directory']}/{task['filename']}"

            self.supervisor.state(
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
                    implementation=self.current_source_code(),
                    specifications=self.storages.docs.get("specifications.md", None),
                )
            )
            self.run([message])

    @staticmethod
    def _agent_node(state, agent: AgentExecutor, name):
        result = agent.invoke(state)
        return {"messages": [Message.create_human_message(result["output"], name=name)]}
