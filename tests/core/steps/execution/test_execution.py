# tests/core/steps/execution/test_execution.py

import unittest
from unittest.mock import MagicMock, patch

from unittest.mock import MagicMock, patch
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.steps.execution.execution import Execution
from gpt_all_star.core.steps.execution.execution import Execution


class TestExecution(unittest.TestCase):
    def setUp(self):
        self.agents = Agents()
        self.execution = Execution(self.agents, False, False, False)

    def test_init_execution(self):
        execution = Execution(self.agents, False, False, False)
        self.assertEqual(execution.agents, self.agents)
        self.assertFalse(execution.japanese_mode)
        self.assertFalse(execution.review_mode)
        self.assertFalse(execution.debug_mode)

    def test_run_successful_execution(self):
        # Mock confirm_execution method
        self.agents.qa_engineer.confirm_execution = MagicMock()

        # Mock run_command method
        self.agents.qa_engineer.run_command = MagicMock()

        # Mock present_choices method
        self.agents.copilot.present_choices = MagicMock(return_value="yes")

        # Mock Improvement class
        with patch("gpt_all_star.core.steps.execution.execution.Improvement") as mock_improvement:
            self.execution.run()

            # Assert that confirm_execution is called with the correct arguments
            self.agents.qa_engineer.confirm_execution.assert_called_with(
                review_mode=False,
                command=self.agents.qa_engineer.storages.root["run.sh"],
            )

            # Assert that run_command is called
        # Test interaction between Execution and Agents classes
        def test_execution_agents_interaction(self):
            # Mock confirm_execution method
            self.agents.qa_engineer.confirm_execution = MagicMock()

            # Mock run_command method
            self.agents.qa_engineer.run_command = MagicMock()

            # Mock present_choices method
            self.agents.copilot.present_choices = MagicMock(return_value="yes")

            # Mock Improvement class
            with patch("gpt_all_star.core.steps.execution.execution.Improvement") as mock_improvement:
                self.execution.run()

                # Assert that confirm_execution is called with the correct arguments
                self.agents.qa_engineer.confirm_execution.assert_called_with(
                    review_mode=False,
                    command=self.agents.qa_engineer.storages.root["run.sh"],
                )

            # Assert that run_command is called
            self.agents.qa_engineer.run_command.assert_called()
            self.assertEqual(self.agents.qa_engineer.run_command.call_count, 1)

                # Assert that present_choices is called with the correct arguments
                self.agents.copilot.present_choices.assert_called_with(
                    "Do you want to improve your source code again?",
                    ["yes", "no"],
                    default=1,
                )

                # Assert that Improvement class is instantiated and run method is called
                mock_improvement.assert_called_with(self.agents, False, False, False)
                mock_improvement.return_value.run.assert_called()
            self.agents.qa_engineer.run_command.assert_called()

            # Assert that present_choices is called with the correct arguments
            self.agents.copilot.present_choices.assert_called_with(
                "Do you want to improve your source code again?",
                ["yes", "no"],
                default=1,
            )

            # Assert that Improvement class is instantiated and run method is called
            mock_improvement.assert_called_with(self.agents, False, False, False)
            mock_improvement.return_value.run.assert_called()
            mock_improvement.assert_called_with(
                self.agents, False, False, False
            )
            mock_improvement.return_value.run.assert_called()

    def test_run_exception_handling_new_case(self):
        # Mock confirm_execution method
        self.agents.qa_engineer.confirm_execution = MagicMock()

        # Mock run_command method to raise an exception
        self.agents.qa_engineer.run_command = MagicMock(side_effect=Exception("Something went wrong"))

        # Mock Team class
        with patch("gpt_all_star.core.steps.execution.team.Team") as mock_team:
            self.execution.run()

            # Assert that confirm_execution is called with the correct arguments
            self.agents.qa_engineer.confirm_execution.assert_called_with(
                review_mode=False,
                command=self.agents.qa_engineer.storages.root["run.sh"],
            )

            # Assert that run_command is called
            self.agents.qa_engineer.run_command.assert_called()

            # Assert that Team class is instantiated and drive method is called
            mock_team.assert_called_with(
                supervisor=self.agents.project_manager,
                members=[
                    self.agents.engineer,
                    self.agents.designer,
                    self.agents.qa_engineer,
                ],
            )
            mock_team.return_value.drive.assert_called()

    def test_run_choice_no(self):
        # Mock confirm_execution method
        self.agents.qa_engineer.confirm_execution = MagicMock()

        # Mock run_command method
        self.agents.qa_engineer.run_command = MagicMock()

        # Mock present_choices method to return "no"
        self.agents.copilot.present_choices = MagicMock(return_value="no")

        # Mock Improvement class
        with patch("gpt_all_star.core.steps.execution.execution.Improvement") as mock_improvement:
            self.execution.run()

            # Assert that confirm_execution is called with the correct arguments
            self.agents.qa_engineer.confirm_execution.assert_called_with(
                review_mode=False,
                command=self.agents.qa_engineer.storages.root["run.sh"],
            )

            # Assert that run_command is called
            self.agents.qa_engineer.run_command.assert_called()

            # Assert that present_choices is called with the correct arguments
            self.agents.copilot.present_choices.assert_called_with(
                "Do you want to improve your source code again?",
                ["yes", "no"],
                default=1,
            )

            # Assert that Improvement class is not instantiated
            mock_improvement.assert_not_called()

if __name__ == "__main__":
    unittest.main()
