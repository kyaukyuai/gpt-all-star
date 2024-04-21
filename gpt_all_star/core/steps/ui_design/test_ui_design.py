from gpt_all_star.core.steps.ui_design.ui_design import UIDesign

def test_implementation_prompt():
    ui_design = UIDesign(...)
    
    prompt = ui_design.implementation_prompt("Test task", "Test context")
    
    assert "Test task" in prompt
    assert "Test context" in prompt
    assert "specifications.md" in prompt
    assert "technologies.md" in prompt