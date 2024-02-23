import pytest
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.development.development import Development
from gpt_all_star.core.steps.development.planning_prompt import planning_prompt_template


class TestDevelopment:
    def test_planning_prompt(self):
        copilot = Copilot()
        development = Development(copilot)

        # Test case 1: specifications, technologies, and files exist
        copilot.storages.docs.get = lambda key, default: "value"
        expected_prompt = "Planning prompt: value, value, value"
        assert development.planning_prompt() == expected_prompt

        # Test case 2: specifications, technologies, and files do not exist
        copilot.storages.docs.get = lambda key, default: "N/A"
        expected_prompt = "Planning prompt: N/A, N/A, N/A"
        assert development.planning_prompt() == expected_prompt

    def test_additional_tasks(self):
        copilot = Copilot()
        development = Development(copilot)

        # Test case 1: additional tasks exist
        expected_tasks = []
        assert development.additional_tasks() == expected_tasks

    def test_callback(self):
        copilot = Copilot()
        development = Development(copilot)

        # Test case: callback method does not return anything, so we can only check if it runs without errors
        development.callback()

if __name__ == "__main__":
    pytest.main()
