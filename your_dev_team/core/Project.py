from __future__ import annotations

import os.path
from pathlib import Path
from rich.table import Table

from your_dev_team.cli.Terminal import ConsoleTerminal
from your_dev_team.core.agents.Agents import Agents
from your_dev_team.core.agents.Architect import Architect
from your_dev_team.core.agents.Engineer import Engineer
from your_dev_team.core.steps.Steps import StepType, STEPS
from your_dev_team.core.Storage import Storage, Storages
from your_dev_team.core.agents.ProductOwner import ProductOwner
from your_dev_team.logger.logger import logger


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
            docs=Storage(project_path / "docs"),
            archive=Storage(project_path / ".archive"),
        )

        self.agents = Agents(
            product_owner=ProductOwner(storages=self.storages),
            engineer=Engineer(storages=self.storages),
            architect=Architect(storages=self.storages),
        )

        self.step_type = self.args['step'] or StepType.DEFAULT
        if self.step_type is StepType.DEFAULT:
            logger.info("archive previous storages")
            Storages.archive_storage(self.storages)

        self.terminal = ConsoleTerminal()
        self.terminal.panel("your-dev-team")
        table = Table(show_header=True, header_style="magenta",title="Members")
        table.add_column("Name")
        table.add_column("Position")
        table.add_column("Description")
        for agent in vars(self.agents).values():
            table.add_row("Taro Yamada", agent.role, "...")
        self.terminal.print(table)


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

    def finish(self) -> None:
        ConsoleTerminal().ask_user(
            "Project is finished! Do you want to add any features or changes?"
            " If yes, describe it here and if no, just press ENTER",
            require_some_input=False)
        logger.info(f"Completed project: {self.name}")
        return
