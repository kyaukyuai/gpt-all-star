import subprocess

from termcolor import colored
from langchain_core.messages import BaseMessage

from your_dev_team.core.Message import Message
from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.steps.Step import Step
from your_dev_team.logger.logger import logger


class Execution(Step):
    def __init__(self, agents: Agents, storages: Storages) -> None:
        super().__init__(agents, storages)

    def run(self) -> list[BaseMessage]:
        command = self.storages.src["run.sh"]

        print()
        print(colored(
            "Do you want to execute this code? (y/n)",
            "red",
        ))
        print()
        print(command)
        print()
        if input().lower() not in ["", "y", "yes"]:
            print("Ok, not executing the code.")
            return []
        print("Executing the code...")
        print()
        print(
            colored(
                "Note: If it does not work as expected, please consider running the code"
                + " in another way than above.", "green"))
        print()
        print("You can press ctrl+c *once* to stop the execution.")
        print()

        command = "bash run.sh"
        try:
            subprocess.run(
                command, shell=True, cwd=self.storages.src.path,
                check=True, text=True, stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError as e:
            user_input = "Please modify the source code based on the error wording above."
            count = 0

            self.terminal.print(f"The following error occurred:\n{e.stderr}.\n Attempt to correct the source codes.\n",
                                style="bold red")
            for file_name, file_str in self._get_code_strings().items():
                self.terminal.print(f"Adding file {file_name} to the prompt...", style="blue")
                code_input = format_file_to_input(file_name, file_str)
                self.agents.engineer.messages.append(Message.create_system_message(f"{code_input}"))

            self.agents.engineer.messages.append(Message.create_system_message(e.stderr))

            self.agents.engineer.chat(user_input)
            response = self.agents.engineer.latest_message_content()
            logger.info(f"response: {response}")
            self.terminal.new_lines(1)
            count += 1

            self.storages.memory['self_healing'] = Message.serialize_messages(
                self.agents.engineer.messages)

            files = Message.parse_message(self.agents.engineer.latest_message_content())
            for file_name, file_content in files:
                self.storages.src[file_name] = file_content

            self.run()

        except KeyboardInterrupt:
            self.terminal.new_lines(1)
            self.terminal.print("Stopping execution.", style="bold yellow")
            self.terminal.print("Execution stopped.", style="bold red")
            self.terminal.new_lines(1)

        return []

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


def format_file_to_input(file_name: str, file_content: str) -> str:
    file_str = f"""
    {file_name}
    ```
    {file_content}
    ```
    """
    return file_str
