import random
import string
import subprocess
import threading
import time
import unittest
from unittest.mock import MagicMock, patch

import requests
from gpt_all_star.core.agents.copilot import Copilot, subprocess, requests, webdriver, Options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class TestCopilot(unittest.TestCase):
    def setUp(self):
        self.copilot = Copilot()

    def tearDown(self):
        pass

    def test_run_command_success(self):
        # Mock subprocess.Popen and simulate successful execution
        mock_process = MagicMock()
        mock_process.wait.return_value = 0
        mock_process.stdout.readline.side_effect = [
            b"Output line 1\n",
            b"Output line 2\n",
            b"",
        ]
        mock_process.stderr.readline.side_effect = [
            b"Error line 1\n",
            b"Error line 2\n",
            b"",
        ]
        mock_popen = MagicMock(return_value=mock_process)
        with patch("subprocess.Popen", mock_popen):
            self.copilot.run_command()

        # Assert that the expected subprocess.Popen arguments were used
        mock_popen.assert_called_once_with(
            "cd ./app && bash ./run.sh",
            shell=True,
            cwd=self.copilot.storages.root.path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_run_command_failure(self):
        # Mock subprocess.Popen and simulate failure
        mock_process = MagicMock()
        mock_process.wait.return_value = 1
        mock_process.stdout.readline.side_effect = [
            b"Output line 1\n",
            b"Output line 2\n",
            b"",
        ]
        mock_process.stderr.readline.side_effect = [
            b"Error line 1\n",
            b"Error line 2\n",
            b"",
        ]
        mock_popen = MagicMock(return_value=mock_process)
        with patch("subprocess.Popen", mock_popen):
            with self.assertRaises(Exception):
                self.copilot.run_command()

        # Assert that the expected subprocess.Popen arguments were used
        mock_popen.assert_called_once_with(
            "cd ./app && bash ./run.sh",
            shell=True,
            cwd=self.copilot.storages.root.path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_run_command_keyboard_interrupt(self):
        # Mock subprocess.Popen and simulate keyboard interrupt
        mock_process = MagicMock(side_effect=KeyboardInterrupt)
        mock_popen = MagicMock(return_value=mock_process)
        with patch("subprocess.Popen", mock_popen):
            with self.assertRaises(KeyboardInterrupt):
                self.copilot.run_command()

        # Assert that the expected subprocess.Popen arguments were used
        mock_popen.assert_called_once_with(
            "cd ./app && bash ./run.sh",
            shell=True,
            cwd=self.copilot.storages.root.path,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_wait_for_server_success(self):
        # Mock requests.get and simulate successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get = MagicMock(return_value=mock_response)
        with patch("requests.get", mock_get):
            result = self.copilot._wait_for_server()

        self.assertTrue(result)

    def test_wait_for_server_failure(self):
        # Mock requests.get and simulate connection error
        mock_get = MagicMock(side_effect=requests.ConnectionError)
        with patch("requests.get", mock_get):
            result = self.copilot._wait_for_server()

        self.assertFalse(result)

    def test_check_browser_errors(self):
        # Mock webdriver.Chrome and simulate console errors
        mock_entry = {"level": "SEVERE", "message": "Error message"}
        mock_get_log = MagicMock(return_value=[mock_entry])
        mock_driver = MagicMock()
        mock_driver.get_log = mock_get_log
        mock_options = MagicMock()
        mock_options.add_argument.return_value = mock_options
        mock_chrome = MagicMock(return_value=mock_driver)
        with patch("selenium.webdriver.Chrome", mock_chrome):
            with patch("selenium.webdriver.chrome.options.Options", mock_options):
                with self.assertRaises(Exception):
                    self.copilot._check_browser_errors()

        # Assert that the expected webdriver.Chrome arguments were used
        mock_chrome.assert_called_once_with(options=mock_options)
        mock_driver.get.assert_called_once_with("http://localhost:3000")

if __name__ == "__main__":
    unittest.main()
