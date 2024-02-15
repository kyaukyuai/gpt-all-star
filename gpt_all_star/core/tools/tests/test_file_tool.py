import unittest
from unittest.mock import MagicMock, patch

from gpt_all_star.core.tools.file_tool import UpdateFileTool


class TestUpdateFileTool(unittest.TestCase):
    @patch("gpt_all_star.core.tools.file_tool.UpdateFileTool.get_relative_path")
    @patch("builtins.open")
    def test_insert_text_at_line_number(self, mock_open, mock_get_relative_path):
        # Mock the file path and inserts
        file_path = "test_file.txt"
        inserts = {1: "Line 1", 3: "Line 3"}

        # Mock the file content
        file_content = ["Line 1\n", "Line 2\n", "Line 3\n"]
        mock_file = MagicMock()
        mock_file.readlines.return_value = file_content
        mock_open.return_value.__enter__.return_value = mock_file

        # Mock the update path
        mock_get_relative_path.return_value = "test_file.txt"

        # Create an instance of UpdateFileTool
        update_file_tool = UpdateFileTool()

        # Call the _run() method
        result = update_file_tool._run(file_path, inserts)

        # Assert the file is updated correctly
        expected_content = ["Line 1\n", "Line 1\n", "Line 2\n", "Line 3\n", "Line 3\n"]
        mock_file.writelines.assert_called_once_with(expected_content)

        # Assert the expected output is returned
        expected_output = "Document edited and saved to test_file.txt"
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
