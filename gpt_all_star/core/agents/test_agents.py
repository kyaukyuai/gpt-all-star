from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.agent import Agent

def test_get_agent_by_role():
    agents = Agents(...)
    
    architect = agents.get_agent_by_role("Architect")
    assert isinstance(architect, Agent)
    assert architect.role.name == "Architect"

def test_set_executors():
    agents = Agents(...)
    
    agents.set_executors("/test/working/directory")
    
    for agent in agents.to_array():
        assert agent.executor.working_directory == "/test/working/directory"