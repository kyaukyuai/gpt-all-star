from gpt_all_star.core.agents.agent import Agent
from gpt_all_star.core.message import Message
from gpt_all_star.core.team import AgentExecutor, Optional


class TeamDocstrings:
    """
    This class contains docstrings for the methods in the Team class.
    """

    def __init__(self, supervisor: Agent, members: list[Agent]):
        """
        Initializes a Team object with a supervisor and a list of members.

        Args:
            supervisor (Agent): The supervisor agent.
            members (list[Agent]): The list of member agents.
        """
        pass

    def _create_supervisor_chain(self):
        """
        Creates a supervisor chain for the team.

        Returns:
            The supervisor chain.
        """
        pass

    def _initialize_state_graph(self):
        """
        Initializes the state graph for the team.

        Returns:
            The initialized state graph.
        """
        pass

    def _add_node_to_graph(self, agent: Agent, state_graph):
        """
        Adds a node to the state graph for the given agent.

        Args:
            agent (Agent): The agent to add to the state graph.
            state_graph: The state graph to add the node to.
        """
        pass

    def _add_edges_to_graph(self, state_graph):
        """
        Adds edges to the state graph for the team members.

        Args:
            state_graph: The state graph to add the edges to.
        """
        pass

    def _add_entry_point_to_graph(self, state_graph):
        """
        Adds an entry point to the state graph.

        Args:
            state_graph: The state graph to add the entry point to.
        """
        pass

    def current_source_code(self):
        """
        Returns the current source code of the supervisor agent.

        Returns:
            The current source code.
        """
        pass

    def storages(self):
        """
        Returns the storages of the supervisor agent.

        Returns:
            The storages.
        """
        pass

    def run(self, messages: list[Message]):
        """
        Runs the team by streaming messages through the state graph.

        Args:
            messages (list[Message]): The list of messages to stream.

        Raises:
            GraphRecursionError: If the recursion limit is reached.
        """
        pass

    def drive(
        self,
        planning_prompt: Optional[str] = None,
        additional_tasks: list[str] = [],
    ):
        """
        Drives the team by creating a planning chain and executing tasks.

        Args:
            planning_prompt (Optional[str], optional): The planning prompt. Defaults to None.
            additional_tasks (list[str], optional): Additional tasks to be added to the plan. Defaults to [].
        """
        pass

    @staticmethod
    def _agent_node(state, agent: AgentExecutor, name):
        """
        Executes the agent node in the state graph.

        Args:
            state: The state of the agent node.
            agent (AgentExecutor): The agent executor.
            name: The name of the agent.

        Returns:
            The output of the agent node.
        """
        pass
