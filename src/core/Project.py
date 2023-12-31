from __future__ import annotations

import os.path
from pathlib import Path

from cli.prompt_toolkit import ask_user
from core.agents.Agents import Agents
from core.agents.Engineer import Engineer
from core.steps.Steps import StepType, STEPS
from core.Storage import Storage, Storages
from core.agents.ProductOwner import ProductOwner
from logger.logger import logger


class Project:
    def __init__(
            self,
            args: dict,
            name: str | None = None,
            description: str | None = None,
            current_step: str | None = None
    ) -> None:
        self.args: dict = args
        self.name: str | None = name
        self.description: str | None = description
        self.current_step: str | None = current_step

        project_path = Path(os.path.abspath('projects/example')).absolute()
        self.storages = Storages(
            origin=Storage(project_path),
            memory=Storage(project_path / "memory"),
            src=Storage(project_path / "src"),
            archive=Storage(project_path / ".archive"),
        )

        self.agents = Agents(
            product_owner=ProductOwner(),
            engineer=Engineer(),
        )

        self.steps = STEPS[self.args['step']] if self.args['step'] is not None else STEPS[StepType.DEFAULT]
        if self.steps in [StepType.DEFAULT]:
            Storages.archive_storage(self.storages)

    def start(self) -> None:
        try:
            for step in self.steps:
                try:
                    step(self.agents, self.storages).run()
                except Exception as e:
                    logger.error(f"Failed to execute step {step}. Reason: {str(e)}")
                    raise e
        except KeyboardInterrupt:
            logger.info("Interrupt received! Stopping...")
            pass

    def finish(self) -> None:
        ask_user(self,
                 "Project is finished! Do you want to add any features or changes? If yes, describe it here and if "
                 "no, just press ENTER",
                 require_some_input=False)
        return
