from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agent import Agent, AgentRole, NEXT_COMMAND
from your_dev_team.logger.logger import logger


class Copilot(Agent):
    def __init__(self, storages: Storages) -> None:
        super().__init__(AgentRole.COPILOT, storages)

    def finish(self) -> None:
        self.ask(
            "Project is finished! Do you want to add any features or changes?"
            " If yes, describe it here and if no, just press ENTER",
            require_answer=False,
        )
        logger.info(f"Completed project: {self.name}")
