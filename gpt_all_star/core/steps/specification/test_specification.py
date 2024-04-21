from gpt_all_star.core.steps.specification.specification import Specification

def test_implementation_prompt():
    specification = Specification(...)
    
    prompt = specification.implementation_prompt("Test task", "Test context")
    
    assert "Test task" in prompt
    assert "Test context" in prompt