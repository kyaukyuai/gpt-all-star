import os
import random
import signal
import string
import subprocess
import threading
import time
from typing import Optional

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.storage import Storages
from gpt_all_star.helper.config_loader import load_configuration
from gpt_all_star.helper.translator import create_translator

APP_TYPES = ["Client-Side Web Application", "Full-Stack Web Application"]


class Copilot(Agent):
    def __init__(
        self,
        storages: Storages | None = None,
        debug_mode: bool = False,
        name: str | None = None,
        profile: str | None = None,
        language: str | None = None,
    ) -> None:
        super().__init__(
            AgentRole.COPILOT, storages, debug_mode, name, profile, language=language
        )
        self._ = create_translator(language)

    def start(self, project_name: str) -> None:
        self.state(self._("Let's start the project! (%s)") % project_name)

    def finish(self, project_name: str) -> None:
        self.state(self._("Completed the project! (%s)") % project_name)

    def ask_project_name(self) -> str:
        default_project_name = "".join(
            random.choice(string.ascii_letters + string.digits) for i in range(15)
        )
        project_name = self.ask(
            self._("What is the name of the project?"),
            is_required=False,
            default=default_project_name,
        )
        return project_name

    def confirm(self, confirmation: str) -> bool:
        CONFIRM_CHOICES = [self._("yes"), self._("no")]
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
            self._(
                "What application do you want to build? Please describe it in as much detail as possible."
            )
        )

    def get_app_type(self) -> str:
        instructions = self.load_instructions()
        app_type = instructions.get("app_type")
        if app_type:
            return app_type
        return self.present_choices(
            self._("What type of application do you want to build?"),
            APP_TYPES,
            default=1,
        )

    def caution(self, command: str) -> None:
        self.state(self._("Executing command: %s") % command)
        self.state(
            self._(
                "If it does not work as expected, please consider running the code"
                + " in another way than above."
            )
        )
        self.console.print(
            self._("You can press ctrl+c *once* to stop the execution."), style="red"
        )

    def run_command(self, command: str, display: bool = True):
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=self.storages.app.path,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,
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

            if url := self._wait_for_server():
                self._check_browser_errors(url)
                if not display:
                    os.killpg(process.pid, signal.SIGTERM)
                    process.wait()
                    return url

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

            os.killpg(process.pid, signal.SIGTERM)
            process.wait()
        except KeyboardInterrupt:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait()
            self._handle_keyboard_interrupt()
            raise KeyboardInterrupt

    def _wait_for_server(self) -> Optional[str]:
        MAX_ATTEMPTS = 30
        for attempt in range(MAX_ATTEMPTS):
            try:
                url = "http://localhost:3000"
                response = requests.get(url)
                if response.status_code == 200:
                    return url
            except requests.ConnectionError:
                pass
            time.sleep(1)
        self.state(self._("Unable to confirm server startup"))
        return None

    def _check_browser_errors(self, url: str) -> None:
        """Access the site with a headless browser and catch console errors"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        errors = ""
        for entry in driver.get_log("browser"):
            if entry["level"] == "SEVERE":
                self.console.print(f"Error: {entry['message']}", style="red")
                errors += f"{entry['message']}\n"
        driver.quit()
        if errors:
            raise Exception({"browser errors": errors})

    def _handle_keyboard_interrupt(self) -> None:
        self.state(self._("Execution stopped."))
