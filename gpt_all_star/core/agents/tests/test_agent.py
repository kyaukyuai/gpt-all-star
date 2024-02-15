import unittest
from unittest.mock import MagicMock, patch

from gpt_all_star.core.agents.agent import Agent
from gpt_all_star.core.tools.file_tool import UpdateFileTool


class TestAgent(unittest.TestCase):
    @patch("gpt_all_star.core.tools.file_tool.UpdateFileTool")
    def test_update_file_tool_import(self, mock_update_file_tool):
        # Create an instance of Agent
        agent = Agent()

        # Assert that the UpdateFileTool is being used correctly
        self.assertIsInstance(agent.tools[-2], UpdateFileTool)
        self.assertEqual(agent.tools[-2].name, "update_file")

        # Assert that the UpdateFileTool is producing the expected results
        mock_update_file_tool_instance = mock_update_file_tool.return_value
        mock_update_file_tool_instance._run.return_value = "Document edited and saved to test_file.txt"
        result = agent.tools[-2]._run("test_file.txt", {1: "Line 1", 3: "Line 3"})
        self.assertEqual(result, "Document edited and saved to test_file.txt")


if __name__ == "__main__":
    unittest.main()
