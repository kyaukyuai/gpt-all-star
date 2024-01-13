from __future__ import annotations

import os.path
from pathlib import Path
from your_dev_team.cli.ConsoleTerminal import ConsoleTerminal

from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.agents.Architect import Architect
from your_dev_team.core.agents.Copilot import Copilot
from your_dev_team.core.agents.Engineer import Engineer
from your_dev_team.core.steps.Steps import StepType, STEPS
from your_dev_team.core.Storage import Storage, Storages
from your_dev_team.core.agents.ProductOwner import ProductOwner
from your_dev_team.logger.logger import logger


class Project:
    def __init__(
        self,
        args: dict,
    ) -> None:
        self.args: dict = args
        self.name = (
            self.args["project_name"]
            or Copilot(
                storages=None, name="copilot", profile="this is copilot"
            ).ask_project_name()
        )

        project_path = Path(os.path.abspath(f"projects/{self.name}")).absolute()
        self.storages = Storages(
            origin=Storage(project_path),
            memory=Storage(project_path / "memory"),
            src=Storage(project_path / "src"),
            docs=Storage(project_path / "docs"),
            archive=Storage(project_path / ".archive"),
        )

        self.agents = Agents(
            copilot=Copilot(
                storages=self.storages, name="copilot", profile="this is copilot"
            ),
            product_owner=ProductOwner(storages=self.storages),
            engineer=Engineer(storages=self.storages),
            architect=Architect(storages=self.storages),
        )

        self.step_type = self.args["step"] or StepType.DEFAULT
        if self.step_type is StepType.DEFAULT:
            logger.info("archive previous storages")
            Storages.archive_storage(self.storages)

    def start(self) -> None:
        self.agents.copilot.start(self.name)
        try:
            for step in STEPS[self.step_type]:
                try:
                    step(self.agents).run()
                except Exception as e:
                    logger.error(f"Failed to execute step {step}. Reason: {str(e)}")
                    raise e
        except KeyboardInterrupt:
            logger.info("Interrupt received! Stopping...")
            pass

    def finish(self) -> None:
        self.agents.copilot.finish()
        pass
