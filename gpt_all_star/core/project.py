from __future__ import annotations

import os.path
import time
from pathlib import Path

from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.architect import Architect
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.agents.designer import Designer
from gpt_all_star.core.agents.engineer import Engineer
from gpt_all_star.core.agents.product_owner import ProductOwner
from gpt_all_star.core.agents.project_manager import ProjectManager
from gpt_all_star.core.agents.qa_engineer import QAEngineer
from gpt_all_star.core.deployment.deployment import Deployment
from gpt_all_star.core.execution.execution import Execution
from gpt_all_star.core.steps.steps import STEPS, StepType
from gpt_all_star.core.storage import Storage, Storages
from gpt_all_star.core.team import Team


class Project:
    def __init__(
        self,
        step: StepType = StepType.DEFAULT,
        project_name: str = None,
        japanese_mode: bool = False,
        review_mode: bool = False,
        debug_mode: bool = False,
    ) -> None:
        self.copilot = Copilot()
        self.start_time = None
        self._set_modes(japanese_mode, review_mode, debug_mode)
        self._set_project_name(project_name)
        self._set_storages()
        self._set_copilot()
        self._set_agents()
        self._set_step_type(step)

    def _set_modes(
        self, japanese_mode: bool, review_mode: bool, debug_mode: bool
    ) -> None:
        self.japanese_mode = japanese_mode
        self.review_mode = review_mode
        self.debug_mode = debug_mode

    def _set_project_name(self, project_name: str) -> None:
        self.project_name = project_name or self.copilot.ask_project_name()

    def _set_storages(self) -> None:
        project_path = Path(os.path.abspath(f"projects/{self.project_name}")).absolute()
        self.storages = Storages(
            root=Storage(project_path),
            docs=Storage(project_path / "docs"),
            app=Storage(project_path / "app"),
            archive=Storage(project_path / ".archive"),
        )

    def _set_copilot(self) -> None:
        self.copilot.storages = self.storages
        self.copilot.debug_mode = self.debug_mode

    def _set_agents(self) -> None:
        self.agents = Agents(
            product_owner=ProductOwner(
                storages=self.storages, debug_mode=self.debug_mode
            ),
            engineer=Engineer(storages=self.storages, debug_mode=self.debug_mode),
            architect=Architect(storages=self.storages, debug_mode=self.debug_mode),
            designer=Designer(storages=self.storages, debug_mode=self.debug_mode),
            qa_engineer=QAEngineer(storages=self.storages, debug_mode=self.debug_mode),
            project_manager=ProjectManager(
                storages=self.storages, debug_mode=self.debug_mode
            ),
        )

    def _set_step_type(self, step: StepType) -> None:
        self.step_type = step or StepType.DEFAULT
        if self.step_type is StepType.DEFAULT:
            self.copilot.state("Archiving previous results...")
            self.storages.archive_storage()

    def _execute_steps(self) -> None:
        try:
            for step in STEPS[self.step_type]:
                self._execute_step(step)
        except KeyboardInterrupt:
            self.copilot.state("Interrupt received! Stopping...")

    def _execute_step(self, step) -> None:
        try:
            self.team.run(step(self.copilot))
        except Exception as e:
            self.copilot.state(f"Failed to execute step {step}. Reason: {str(e)}")
            raise e

    def start(self) -> None:
        self.start_time = time.time()
        self.copilot.start(self.project_name)
        self.team = Team(
            copilot=self.copilot,
            members=self.agents,
            japanese_mode=self.japanese_mode,
        )
        self._execute_steps()
        if self.copilot.confirm("Do you want to execute this application?"):
            Execution(self.team, self.copilot).run()
        if self.copilot.confirm(
            "Do you want to manage this application code with GitHub?"
        ):
            Deployment(self.copilot).run()

    def finish(self) -> None:
        if self.start_time:
            end_time = time.time()
            elapsed_time = end_time - self.start_time
            self.copilot.state(
                f"Project finished. Elapsed time: {elapsed_time:.2f} seconds."
            )
        self.copilot.finish(self.project_name)
