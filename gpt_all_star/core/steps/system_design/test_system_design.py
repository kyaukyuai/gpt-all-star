from gpt_all_star.core.steps.system_design.system_design import SystemDesign

def test_implementation_prompt():
    system_design = SystemDesign(...)

    prompt = system_design.implementation_prompt("Test task", "Test context")

    assert "Test task" in prompt
    assert "Test context" in prompt
    assert "specifications.md" in prompt