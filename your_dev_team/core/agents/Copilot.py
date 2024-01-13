import os
import subprocess
import git
import requests
from termcolor import colored

from your_dev_team.core.Message import Message
from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agent import Agent, AgentRole
from your_dev_team.logger.logger import logger


class Copilot(Agent):
    def __init__(self, storages: Storages, name: str, profile: str) -> None:
        super().__init__(AgentRole.COPILOT, storages, name, profile)

    def start(self) -> None:
        self._console.panel("your-dev-team")

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
            user_input = (
                "Please modify the source code based on the error wording above."
            )
            count = 0

            self._console.print(
                f"The following error occurred:\n{e.stderr}.\n Attempt to correct the source codes.\n",
                style="bold red",
            )
            for file_name, file_str in self._get_code_strings().items():
                self._console.print(
                    f"Adding file {file_name} to the prompt...", style="blue"
                )
                code_input = format_file_to_input(file_name, file_str)
                self.messages.append(Message.create_system_message(f"{code_input}"))

            self.messages.append(Message.create_system_message(e.stderr))

            self.chat(user_input)
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
        files_dict = {}

        for path in self.storages.src.path.iterdir():
            if path.is_file():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                except UnicodeDecodeError:
                    raise ValueError(
                        f"Non-text file detected: {path}, datable-interpreter currently only supports utf-8 "
                        f"decidable text"
                        f"files."
                    )

            files_dict[path] = file_content

        return files_dict

    def git_push(self) -> None:
        self.state("Pushing to the repository...")
        repo_path = self.storages.src.path
        repo = git.Repo.init(repo_path)
        files_to_add = [str(file) for file in repo_path.iterdir() if file.is_file()]
        if not files_to_add:
            logger.info("No files to add to the repository.")
            return

        repo.index.add(files_to_add)
        repo.index.commit("Add files via your-dev-team")

        try:
            remote_name = "origin"
            remote_url = "https://github.com/your-dev-team/sample.git"
            if remote_name in repo.remotes:
                remote = repo.remotes[remote_name]
                remote.set_url(remote_url)
            else:
                remote = repo.create_remote(remote_name, remote_url)

            # 現在のブランチ名を取得してプッシュ
            current_branch = repo.active_branch.name
            remote.push(refspec=f"{current_branch}:{current_branch}")
        except Exception as e:
            logger.error(f"Failed to push to the repository: {e}")

    def create_github_repo(self) -> None:
        url = "https://api.github.com/orgs/your-dev-team/repos"
        token = os.getenv("GITHUB_TOKEN")

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        data = {"name": "sample", "private": False}

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 201:
            print("Repository created successfully.")
        else:
            print(
                f"Failed to create repository. Status code: {response.status_code}, {response.text}"
            )


def format_file_to_input(file_name: str, file_content: str) -> str:
    file_str = f"""
    {file_name}
    ```
    {file_content}
    ```
    """
    return file_str
