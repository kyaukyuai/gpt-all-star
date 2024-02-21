import unittest
from unittest.mock import MagicMock

from gpt_all_star.helper.multi_agent_collaboration_graph import \
    MultiAgentCollaborationGraph


class TestMultiAgentCollaborationGraph(unittest.TestCase):
    def setUp(self):
        # Create a supervisor and agents for testing
        self.supervisor = MagicMock()
        self.agents = [MagicMock(), MagicMock()]

        # Create an instance of MultiAgentCollaborationGraph for testing
        self.graph = MultiAgentCollaborationGraph(self.supervisor, self.agents)

    def test_add_node(self):
        # Test adding a node to the state graph
        agent_name = "Agent1"
        agent_executor = MagicMock()
        self.graph._state_graph.add_node = MagicMock()

        self.graph._add_nodes()

        self.graph._state_graph.add_node.assert_called_once_with(
            agent_name,
            MagicMock(
                side_effect=self.graph._agent_node_callback,
                agent=agent_executor,
                name=agent_name,
            ),
        )

    def test_add_edge(self):
        # Test adding an edge to the state graph
        agent_name = "Agent1"
        self.graph._state_graph.add_edge = MagicMock()

        self.graph._add_edges()

        self.graph._state_graph.add_edge.assert_called_once_with(agent_name, "Supervisor")

    def test_add_entry_point(self):
        # Test adding the entry point to the state graph
        self.graph._state_graph.add_node = MagicMock()
        self.graph._state_graph.add_conditional_edges = MagicMock()
        self.graph._state_graph.set_entry_point = MagicMock()

        self.graph._add_entry_point()

        self.graph._state_graph.add_node.assert_called_once_with(
            "Supervisor", self.supervisor.create_supervisor_chain(members=self.agents)
        )
        self.graph._state_graph.add_conditional_edges.assert_called_once_with(
            "Supervisor",
            self.graph._state_graph.compile.return_value.__getitem__.return_value,
            {"Agent1": "Agent1", "Agent2": "Agent2", "FINISH": "END"},
        )
        self.graph._state_graph.set_entry_point.assert_called_once_with("Supervisor")

    def test_agent_node_callback(self):
        # Test the agent node callback function
        state = {"next": "Agent1"}
        agent_executor = MagicMock()
        agent_name = "Agent1"
        agent_output = "Agent1 Output"
        agent_executor.invoke.return_value = {"output": agent_output}

        result = self.graph._agent_node_callback(state, agent_executor, agent_name)

        self.assertEqual(
            result,
            {"messages": [MagicMock.create_human_message.return_value]},
        )
        agent_executor.invoke.assert_called_once_with(state)
        MagicMock.create_human_message.assert_called_once_with(agent_output, name=agent_name)


if __name__ == "__main__":
    unittest.main()
