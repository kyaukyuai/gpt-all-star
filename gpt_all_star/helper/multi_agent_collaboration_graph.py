import functools

from langchain.agents.agent import AgentExecutor
from langgraph.graph import END, StateGraph

from gpt_all_star.core.agents.agent import Agent
from gpt_all_star.core.agents.agent_state import AgentState
from gpt_all_star.core.agents.chain import Chain
from gpt_all_star.core.message import Message

SUPERVISOR_NAME = "Supervisor"


class MultiAgentCollaborationGraph:
    def __init__(self, supervisor: Agent, agents: list[Agent]):
        self.supervisor = supervisor
        self.agents = agents
        self._state_graph = StateGraph(AgentState)
        self._initialize_graph()
        self.workflow = self._state_graph.compile()

    def _initialize_graph(self):
        self._add_nodes()
        self._add_entry_point()
        self._add_edges()

    def _add_nodes(self):
        for agent in self.agents:
            self._state_graph.add_node(
                agent.role.name,
                functools.partial(
                    self._agent_node_callback,
                    agent=agent.executor,
                    name=agent.role.name,
                ),
            )

    def _add_edges(self):
        for agent in self.agents:
            self._state_graph.add_edge(agent.role.name, SUPERVISOR_NAME)

    def _add_entry_point(self):
        self._state_graph.add_node(
            SUPERVISOR_NAME,
            Chain().create_supervisor_chain(members=self.agents),
        )
        conditional_map = {agent.role.name: agent.role.name for agent in self.agents}
        conditional_map["FINISH"] = END
        self._state_graph.add_conditional_edges(
            SUPERVISOR_NAME, lambda state: state["next"], conditional_map
        )
        self._state_graph.set_entry_point(SUPERVISOR_NAME)

    @staticmethod
    def _agent_node_callback(state, agent: AgentExecutor, name):
        result = agent.invoke(state)
        return {"messages": [Message.create_human_message(result["output"], name=name)]}
