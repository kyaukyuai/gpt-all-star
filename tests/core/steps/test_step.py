import unittest
from unittest.mock import patch

from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.step import Step


class TestStep(unittest.TestCase):
    def setUp(self):
        self.agents = Agents()
        self.step = Step(self.agents)

    def test_planning_prompt(self):
        # Test case 1: Test planning prompt with Japanese mode enabled
        self.step.japanese_mode = True
        result = self.step.planning_prompt()
        self.assertEqual(result, "Enter the planning prompt in Japanese")

        # Test case 2: Test planning prompt with Japanese mode disabled
        self.step.japanese_mode = False
        result = self.step.planning_prompt()
        self.assertEqual(result, "Enter the planning prompt in English")

    def test_additional_tasks(self):
        # Test case 1: Test additional tasks with review mode enabled
        self.step.review_mode = True
        result = self.step.additional_tasks()
        self.assertEqual(result, ["Review the additional tasks"])

        # Test case 2: Test additional tasks with review mode disabled
        self.step.review_mode = False
        result = self.step.additional_tasks()
        self.assertEqual(result, ["Complete the additional tasks"])

        # Test case 3: Test additional tasks with debug mode enabled
        self.step.debug_mode = True
        result = self.step.additional_tasks()
        self.assertEqual(result, ["Debug the additional tasks"])

        # Test case 4: Test additional tasks with debug mode disabled
        self.step.debug_mode = False
        result = self.step.additional_tasks()
        self.assertEqual(result, ["Execute the additional tasks"])

if __name__ == "__main__":
    unittest.main()
