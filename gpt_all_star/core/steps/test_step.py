from gpt_all_star.core.steps.step import Step

def test_implementation_prompt():
    step = ConcreteStep(...)
    
    prompt = step.implementation_prompt("Test task", "Test context")
    
    assert "Test task" in prompt
    assert "Test context" in prompt
    assert "specifications.md" in prompt
    assert "technologies.md" in prompt
    assert "ui_design.html" in prompt

class ConcreteStep(Step):
    def assign_prompt(self):
        pass
        
    def planning_prompt(self):
        pass
        
    def additional_tasks(self):
        pass
        
    def callback(self):
        pass
        
    def improvement_prompt(self):
        pass