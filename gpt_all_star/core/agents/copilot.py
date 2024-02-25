import random
import string
import subprocess
import threading
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.storage import Storages
from gpt_all_star.helper.config_loader import load_configuration

APP_TYPES = ["Client-Side Web Application", "Full-Stack Web Application"]


class Copilot(Agent):
    def __init__(
        self,
        storages: Storages | None = None,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.COPILOT, storages, debug_mode, name, profile)

    def start(self, project_name: str) -> None:
        self.state(f"Let's start the project! ({project_name})")

    def finish(self, project_name: str) -> None:
        self.state(f"Completed the project! ({project_name})")

    def ask_project_name(self) -> str:
        default_project_name = "".join(
            random.choice(string.ascii_letters + string.digits) for i in range(15)
        )
        project_name = self.ask(
            "What is the name of the project?",
            is_required=False,
            default=default_project_name,
        )
        return project_name

    def confirm(self, confirmation: str) -> bool:
        CONFIRM_CHOICES = ["yes", "no"]
        choice = self.present_choices(
            confirmation,
            CONFIRM_CHOICES,
            default=1,
        )
        return choice == CONFIRM_CHOICES[0]

    def load_instructions(
        self, file_path: str = "./gpt_all_star/instructions.yml"
    ) -> dict:
        return load_configuration(file_path)

    def get_instructions(self) -> str:
        instructions = self.load_instructions()
        instruction = instructions.get("instruction")
        if instruction:
            return instruction
        return self.ask(
            "What application do you want to build? Please describe it in as much detail as possible."
        )

    def get_app_type(self) -> str:
        instructions = self.load_instructions()
        app_type = instructions.get("app_type")
        if app_type:
            return app_type
        return self.present_choices(
            "What type of application do you want to build?",
            APP_TYPES,
            default=1,
        )

    def caution(self, command: str) -> None:
        self.state(f"Executing command: {command}")
        self.state(
            "If it does not work as expected, please consider running the code"
            + " in another way than above."
        )
        self.console.print(
            "You can press ctrl+c *once* to stop the execution.", style="red"
        )

    def run_command(self, command: str) -> None:
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
            process.wait()
            self._handle_keyboard_interrupt()
            raise KeyboardInterrupt

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
        self.state("Execution stopped.")
