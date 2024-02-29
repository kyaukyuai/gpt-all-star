import unittest
from unittest.mock import MagicMock

from gpt_all_star.core.steps.ui_design.ui_design import UIDesign


class TestUIDesign(unittest.TestCase):
    def setUp(self):
        self.copilot_mock = MagicMock()
        self.ui_design = UIDesign(self.copilot_mock)

    def test_planning_prompt(self):
        # Test planning_prompt method
        expected_prompt = "Test planning prompt"
        self.copilot_mock.storages.current_source_code.return_value = "Test source code"
        self.copilot_mock.storages.docs.get.return_value = "Test specifications.md"
        planning_prompt = self.ui_design.planning_prompt()
        self.assertEqual(planning_prompt, expected_prompt)

    def test_additional_tasks(self):
        # Test additional_tasks method
        expected_tasks = []
        tasks = self.ui_design.additional_tasks()
        self.assertEqual(tasks, expected_tasks)

    def test_callback(self):
        # Test callback method
        expected_result = True
        result = self.ui_design.callback()
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
