from __future__ import annotations

import subprocess
import threading
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.storage import Storages


class QAEngineer(Agent):
    def __init__(
        self,
        storages: Storages,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.QA_ENGINEER, storages, debug_mode, name, profile)

    def confirm_execution(self, review_mode: bool, command: str) -> None:
        if review_mode:
            self.console.new_lines()
            CONFIRM_CHOICES = ["yes", "no"]
            choice = self.present_choices(
                "Do you want to execute this code?",
                CONFIRM_CHOICES,
                default=1,
            )
            self.console.new_lines()
            self.console.print(command)
            self.console.new_lines()
            if choice == CONFIRM_CHOICES[1]:
                print("Ok, not executing the code.")
                return []

        self.state("Executing the code...")
        self.console.new_lines()
        self.state(
            "If it does not work as expected, please consider running the code"
            + " in another way than above."
        )
        self.console.new_lines()
        self.console.print(
            "You can press ctrl+c *once* to stop the execution.", style="red"
        )
        self.console.new_lines()

    def run_command(self) -> None:
        command = "bash run.sh"
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.storages.app.path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout_lines = []
            stderr_lines = []

            def read_stdout():
                for line in iter(process.stdout.readline, ""):
                    stdout_lines.append(line.strip())
                    self.console.print(f"{line.strip()}", style="green")

            def read_stderr():
                for line in iter(process.stderr.readline, ""):
                    stderr_lines.append(line.strip())
                    self.console.print(f"{line.strip()}", style="red")

            stdout_thread = threading.Thread(target=read_stdout)
            stderr_thread = threading.Thread(target=read_stderr)
            stdout_thread.start()
            stderr_thread.start()

            if self._wait_for_server():
                self._check_browser_errors()
                return

            stdout_thread.join()
            stderr_thread.join()

            return_code = process.wait()
            if return_code != 0:
                raise Exception(
                    {
                        "stdout": "\n".join(stdout_lines),
                        "stderr": "\n".join(stderr_lines),
                    }
                )
            process.terminate()
        except KeyboardInterrupt:
            self._handle_keyboard_interrupt()

    def _wait_for_server(self) -> bool:
        MAX_ATTEMPTS = 30
        for attempt in range(MAX_ATTEMPTS):
            try:
                response = requests.get("http://localhost:3000")
                if response.status_code == 200:
                    return True
            except requests.ConnectionError:
                pass
            time.sleep(1)
        self.state("Unable to confirm server startup")
        return False

    def _check_browser_errors(self):
        """Access the site with a headless browser and catch console errors"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://localhost:3000")

        errors = ""
        for entry in driver.get_log("browser"):
            if entry["level"] == "SEVERE":
                self.console.print(f"Error: {entry['message']}", style="red")
                errors += f"{entry['message']}\n"
        driver.quit()
        if errors:
            raise Exception({"browser errors": errors})

    def _handle_keyboard_interrupt(self) -> None:
        self.console.new_lines()
        self.console.print("Stopping execution.", style="bold yellow")
        self.console.print("Execution stopped.", style="bold red")
        self.console.new_lines()
