import unittest
from unittest.mock import patch

from gpt_all_star.core.agents.qa_engineer import QAEngineer


class TestQAEngineer(unittest.TestCase):
    def setUp(self):
        self.qa_engineer = QAEngineer(storages=None)

    def test_confirm_execution_review_mode(self):
        with patch("builtins.input", return_value="no"):
            result = self.qa_engineer.confirm_execution(review_mode=True, command="test command")
            self.assertEqual(result, [])

    def test_confirm_execution_no_review_mode(self):
        with patch("builtins.input", return_value="yes"):
            result = self.qa_engineer.confirm_execution(review_mode=False, command="test command")
            self.assertIsNone(result)

    def test_run_command_success(self):
        with patch("subprocess.Popen") as mock_popen:
            mock_process = mock_popen.return_value
            mock_process.wait.return_value = 0
            result = self.qa_engineer.run_command()
            self.assertIsNone(result)

    def test_run_command_error(self):
        with patch("subprocess.Popen") as mock_popen:
            mock_process = mock_popen.return_value
            mock_process.wait.return_value = 1
            with self.assertRaises(Exception):
                self.qa_engineer.run_command()

if __name__ == "__main__":
    unittest.main()
