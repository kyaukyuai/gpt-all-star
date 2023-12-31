import subprocess

from termcolor import colored
from langchain_core.messages import BaseMessage

from core.Storage import Storages
from core.agents.Agents import Agents
from core.steps.Step import Step


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

        p = subprocess.Popen("bash run.sh", shell=True, cwd=self.storages.src.path)
        try:
            p.wait()
        except KeyboardInterrupt:
            print()
            print("Stopping execution.")
            print("Execution stopped.")
            p.kill()
            print()

        return []
