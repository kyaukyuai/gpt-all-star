import unittest
from unittest.mock import MagicMock

from gpt_all_star.core.deployment.deployment import Deployment
from gpt_all_star.helper.git import Git


class TestDeployment(unittest.TestCase):
    def setUp(self):
        self.storages = MagicMock()
        self.copilot = MagicMock()
        self.deployment = Deployment(self.storages, self.copilot)

    def test_create_pull_request(self):
        git = MagicMock(spec=Git)
        git.check_local_main_branch_exists.return_value = False
        git.diffs.return_value = "diff content"
        git.create_pull_request.return_value = "pull request URL"

        self.deployment.copilot.console.new_lines = MagicMock()
        self.deployment.copilot.state = MagicMock()

        with self.assertRaises(Exception):
            self.deployment.run()

        git.check_local_main_branch_exists.assert_called_once()
        git.checkout.assert_called_once_with("main")
        git.add.assert_called_once()
        git.commit.assert_called_once()
        git.push.assert_called_once()
        git.create_pull_request.assert_called_once_with("main")

    def test_create_pull_request_main_branch(self):
        git = MagicMock(spec=Git)
        git.check_local_main_branch_exists.return_value = True
        git.diffs.return_value = "diff content"

        self.deployment.copilot.console.new_lines = MagicMock()
        self.deployment.copilot.state = MagicMock()

        self.deployment.run()

        git.check_local_main_branch_exists.assert_called_once()
        git.checkout.assert_not_called()
        git.add.assert_called_once()
        git.commit.assert_called_once()
        git.push.assert_called_once()
        git.create_pull_request.assert_not_called()

    def test_create_pull_request_no_files(self):
        git = MagicMock(spec=Git)
        git.files.return_value = []

        self.deployment.copilot.state = MagicMock()

        self.deployment.run()

        git.files.assert_called_once()
        git.check_local_main_branch_exists.assert_not_called()
        git.checkout.assert_not_called()
        git.add.assert_not_called()
        git.commit.assert_not_called()
        git.push.assert_not_called()
        git.create_pull_request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
