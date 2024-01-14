import os
import random
import string
import subprocess
import git
import requests
from termcolor import colored
from rich.syntax import Syntax

from your_dev_team.core.Message import Message
from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agent import Agent, AgentRole
from your_dev_team.core.steps import step_prompts
from your_dev_team.logger.logger import logger


class Copilot(Agent):
    def __init__(self, storages: Storages, name: str, profile: str) -> None:
        super().__init__(AgentRole.COPILOT, storages, name, profile)

    def start(self, project_name: str) -> None:
        self.state(f"Let's start the project! ({project_name})")
        self._console.new_lines(1)

    def ask_project_name(self) -> str:
        default_project_name = "".join(
            random.choice(string.ascii_letters + string.digits) for i in range(15)
        )
        project_name = self.ask(
            "What is the name of the project?",
            require_answer=False,
            default_value=default_project_name,
        )
        return project_name

    def finish(self) -> None:
        self.ask(
            "Project is finished! Do you want to add any features or changes?"
            " If yes, describe it here and if no, just press ENTER",
            require_answer=False,
            default_value=None,
        )

        logger.info(f"Completed project: {self.name}")

    def execute_code(self) -> None:
        command = self.storages.src["run.sh"]

        self._console.new_lines()
        print(
            colored(
                "Do you want to execute this code? (y/n)",
                "red",
            )
        )
        self._console.new_lines()
        print(command)
        self._console.new_lines()
        if input().lower() not in ["", "y", "yes"]:
            print("Ok, not executing the code.")
            return []
        print("Executing the code...")
        self._console.new_lines()
        print(
            colored(
                "Note: If it does not work as expected, please consider running the code"
                + " in another way than above.",
                "green",
            )
        )
        self._console.new_lines()
        print("You can press ctrl+c *once* to stop the execution.")
        self._console.new_lines()

        command = "bash run.sh"
        try:
            subprocess.run(
                command,
                shell=True,
                cwd=self.storages.src.path,
                check=True,
                text=True,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as e:
            count = 0

            self._console.print(
                f"The following error occurred:\n{e.stderr}.\n Attempt to correct the source codes.\n",
                style="bold red",
            )
            for file_name, file_str in self._get_code_strings().items():
                self._console.print(
                    f"Adding file {file_name} to the prompt...", style="blue"
                )
                code_input = step_prompts.format_file_to_input(file_name, file_str)
                self.messages.append(Message.create_system_message(f"{code_input}"))

            self.messages.append(Message.create_system_message(e.stderr))

            self.chat(step_prompts.fix_source_code_template.format())
            response = self.latest_message_content()
            logger.info(f"response: {response}")
            self._console.new_lines(1)
            count += 1

            self.storages.memory["self_healing"] = Message.serialize_messages(
                self.messages
            )

            files = Message.parse_message(self.latest_message_content())
            for file_name, file_content in files:
                self.storages.src[file_name] = file_content

            self.execute_code()

        except KeyboardInterrupt:
            self._console.new_lines(1)
            self._console.print("Stopping execution.", style="bold yellow")
            self._console.print("Execution stopped.", style="bold red")
            self._console.new_lines(1)

    def _get_code_strings(self) -> dict[str, str]:
        return self.storages.src.recursive_file_search()

    def push_to_git_repository(self) -> None:
        self._create_new_github_repository()
        repo_path = self.storages.origin.path
        repo = git.Repo.init(repo_path)
        files_to_add = [
            str(file)
            for file in repo_path.rglob("*")
            if file.is_file()
            and "node_modules" not in str(file)
            and ".git" not in str(file)
            and "memory" not in str(file)
            and ".archive" not in str(file)
        ]
        if not files_to_add:
            logger.info("No files to add to the repository.")
            return

        self.state("The following diff will be pushed to the repository")
        repo_path = self.storages.origin.path
        repo = git.Repo(repo_path)
        diffs = repo.git.diff("HEAD")
        syntax = Syntax(diffs, "diff", theme="monokai", line_numbers=True)
        self._console.print(syntax)

        response = self.ask(
            "Continue with commit and push? (y/n)",
            require_answer=False,
            default_value="y",
        )
        if response.lower() not in ["", "y", "yes"]:
            return

        self.state("Pushing to the repository...")
        repo.index.add(files_to_add)
        repo.index.commit("Add files via your-dev-team")

        try:
            remote_name = "origin"
            remote_url = (
                f"https://github.com/your-dev-team/{self.storages.origin.path.name}.git"
            )
            if remote_name in repo.remotes:
                remote = repo.remotes[remote_name]
                if remote.url != remote_url:
                    remote.set_url(remote_url)
            else:
                remote = repo.create_remote(remote_name, remote_url)

            current_branch = repo.active_branch.name
            remote.push(refspec=f"{current_branch}:{current_branch}")
        except git.exc.GitCommandError as e:
            logger.error(f"Failed to push to the repository: {e}")
            raise e
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise e

    def _create_new_github_repository(self) -> None:
        url = "https://api.github.com/orgs/your-dev-team/repos"
        token = os.getenv("GITHUB_TOKEN")

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        data = {"name": self.storages.origin.path.name, "private": False}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repos = response.json()
            if any(repo["name"] == self.storages.origin.path.name for repo in repos):
                self.state("Repository already exists, skipping creation.")
                return

        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            self.state("Repository created successfully.")
        else:
            self.state(
                f"Failed to create repository. Status code: {response.status_code}, {response.text}"
            )
