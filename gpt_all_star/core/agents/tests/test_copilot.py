import unittest
from unittest.mock import MagicMock

from gpt_all_star.core.agents.copilot import Copilot


class TestCopilot(unittest.TestCase):
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
