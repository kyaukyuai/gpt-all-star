from __future__ import annotations

import os.path
from pathlib import Path

from core.Agents import Agents
from core.Steps import StepType, STEPS
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

        self.step_type = StepType.DEFAULT

        project_path = Path(os.path.abspath('projects/example')).absolute()
        self.storages = Storages(
            origin=Storage(project_path),
            result=Storage(project_path / "result")
        )

        self.agents = Agents(
            product_owner=ProductOwner()
        )

    def start(self) -> None:
        try:
            for step in STEPS[self.step_type]:
                try:
                    step(self.agents, self.storages).run()
                except Exception as e:
                    logger.error(f"Failed to execute step {step}. Reason: {str(e)}")
                    raise e
        except KeyboardInterrupt:
            logger.info("Interrupt received! Stopping...")
            pass
