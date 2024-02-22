import unittest
from unittest.mock import MagicMock

from gpt_all_star.core.agents.tests.test_copilot import Copilot


class TestCopilot(unittest.TestCase):
    def test_ask_project_name(self):
        copilot = Copilot()
        project_name = copilot.ask_project_name()
        self.assertIsInstance(project_name, str, msg='Project name should be a string')
        
    def test_confirm(self):
        copilot = Copilot()
        self.assertTrue(copilot.confirm('yes'))
        self.assertFalse(copilot.confirm('no'))
        
    def test_get_instructions(self):
        copilot = Copilot()
        instructions = copilot.get_instructions()
        self.assertIsInstance(instructions, str, msg='Instructions should be a string')
        
    def test_get_app_type(self):
        copilot = Copilot()
        app_type = copilot.get_app_type()
        self.assertTrue(app_type in ['Client-Side Web Application', 'Full-Stack Web Application'],
                        msg='App type should be one of the predefined types')
        
    def test_caution(self):
        copilot = Copilot()
        self.assertIsNone(copilot.caution(), msg='Caution should return None')
    def test_confirm_push(self):
        # Mock dependencies
        copilot = Copilot()
        copilot.present_choices = MagicMock(return_value="yes")

        # Test confirm_push with different scenarios
        # Scenario 1: Confirmation is "yes"
        self.assertTrue(copilot.confirm_push("yes"))

        # Scenario 2: Confirmation is "no"
        self.assertFalse(copilot.confirm_push("no"))

        # Scenario 3: Confirmation is empty
        self.assertFalse(copilot.confirm_push(""))

        # Scenario 4: Confirmation is invalid
        self.assertFalse(copilot.confirm_push("invalid"))

        # Assert that present_choices is called with the correct arguments
        copilot.present_choices.assert_called_with(
            "yes",
            ["yes", "no"],
            default=1,
        )


if __name__ == "__main__":
    unittest.main()
