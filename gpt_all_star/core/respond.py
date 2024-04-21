from __future__ import annotations

import os.path
from pathlib import Path

from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.architect import Architect
from gpt_all_star.core.agents.chain import ACTIONS, Chain
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.agents.designer import Designer
from gpt_all_star.core.agents.engineer import Engineer
from gpt_all_star.core.agents.product_owner import ProductOwner
from gpt_all_star.core.agents.project_manager import ProjectManager
from gpt_all_star.core.agents.qa_engineer import QAEngineer
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.healing.healing import Healing
from gpt_all_star.core.steps.specification.specification import Specification
from gpt_all_star.core.steps.steps import STEPS, StepType
from gpt_all_star.core.storage import Storage, Storages
from gpt_all_star.helper.git import Git
from gpt_all_star.helper.multi_agent_collaboration_graph import (
    MultiAgentCollaborationGraph,
)
from gpt_all_star.helper.translator import create_translator


class Respond:
    def __init__(
        self,
        step: StepType = StepType.DEFAULT,
        project_name: str = None,
        japanese_mode: bool = False,
        review_mode: bool = False,
        debug_mode: bool = False,
        plan_and_solve: bool = False,
    ) -> None:
        self.copilot = Copilot(language="ja" if japanese_mode else "en")
        self.start_time = None
        self.plan_and_solve = plan_and_solve
        self._set_modes(japanese_mode, review_mode, debug_mode)
        self._set_project_name(project_name)
        self._set_storages()
        self._set_copilot()
        self._set_agents()
        self._set_step_type(step)

        self._ = create_translator("ja" if japanese_mode else "en")

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
        for agent in self.agents.to_array():
            if self.japanese_mode:
                agent.profile += "\n**IMPORTANT: 必ず日本語で書いて下さい**"

    def _set_step_type(self, step: StepType) -> None:
        self.step_type = step or StepType.DEFAULT
        if self.step_type is StepType.DEFAULT:
            if self.debug_mode:
                self.copilot.state(self._("Archiving previous results..."))
            self.storages.archive_storage()

    def deploy(self) -> None:
        git = Git(self.copilot.storages.root.path)
        files_to_add = git.files()
        if not files_to_add:
            yield {
                "messages": [
                    Message.create_human_message(
                        message=self._("No files to add to the repository.")
                    )
                ],
            }
            return
        commit_info = (
            Chain()
            .create_git_commit_message_chain()
            .invoke(
                {
                    "messages": [
                        Message.create_human_message(
                            f"""
# Instructions
---
Generate an appropriate branch name and commit message showing the following diffs.

# Constraints
---
The format should follow Conventional Commits.

## Here is the diff
```
{git.diffs()}
```
"""
                        )
                    ],
                }
            )
        )
        yield {
            "messages": [Message.create_human_message(message=f"{commit_info}")],
        }
        try:
            branch_name = (
                commit_info["branch"]
                if git.check_local_main_branch_exists()
                else "main"
            )
            is_main_branch = branch_name == "main"

            if not is_main_branch:
                git.checkout(branch_name)

            git.add(files_to_add)
            git.commit(commit_info["message"])
            git.push()

            if not is_main_branch:
                git.create_pull_request(branch_name)

            yield {
                "messages": [
                    Message.create_human_message(
                        message=self._("Successfully deployed to the repository: %s")
                        % git.url()
                    )
                ],
            }
        except Exception as e:
            self.copilot.state(
                self._("An error occurred while pushing to the repository: %s") % str(e)
            )

    def execute(self) -> None:
        command = (
            Chain()
            .create_command_to_execute_application_chain()
            .invoke(
                {
                    "messages": [
                        Message.create_human_message(
                            f"""
# Instructions
---
Generate an command to execute the application.

# Constraints
---
- Check the current implementation and directory structure and be sure to launch the application.
- If run.sh exists, it should be used first. To use it, move to the directory where run.sh exists, and then run `sh . /run.sh` after moving to the directory where run.sh exists.

# Current Implementation
---
{self.copilot.storages.current_source_code(debug_mode=self.copilot.debug_mode)}
"""
                        )
                    ],
                }
            )
        )
        yield {
            "messages": [
                Message.create_human_message(
                    message=f"Execute command: {command['command']}"
                )
            ],
        }

        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            try:
                url = self.copilot.run_command(command["command"], display=False)
                execution_info = {
                    "command": command["command"],
                    "url": url,
                }
                yield {
                    "messages": [
                        Message.create_human_message(message=f"{execution_info}")
                    ],
                }
                return
            except Exception as e:
                yield {
                    "messages": [
                        Message.create_human_message(message=f"Error is happened: {e}")
                    ],
                }
                step = Healing(copilot=self.copilot, display=False, error_message=e)
                for agent in self.agents.to_array():
                    agent.set_executor(step.working_directory)
                supervisor_name = (
                    Chain()
                    .create_assign_supervisor_chain(members=self.agents.to_array())
                    .invoke(
                        {
                            "messages": [
                                Message.create_human_message(step.planning_prompt())
                            ]
                        }
                    )
                    .get("assign")
                )
                supervisor = self.agents.get_agent_by_role(supervisor_name)
                self._graph = MultiAgentCollaborationGraph(
                    supervisor, self.agents.to_array()
                )
                self.supervisor = supervisor
                tasks = (
                    Chain()
                    .create_planning_chain(self.supervisor.profile)
                    .invoke(
                        {
                            "messages": [
                                Message.create_human_message(step.planning_prompt())
                            ],
                        }
                    )
                )

                yield {
                    "messages": [
                        Message.create_human_message(
                            message=str(tasks), name=self.supervisor.role.name
                        )
                    ],
                }

                count = 1
                while len(tasks["plan"]) > 0:
                    task = tasks["plan"][0]
                    if task["action"] == ACTIONS[0]:
                        todo = f"{task['action']}: {task['command']} in the directory({task.get('working_directory', '')})"
                    else:
                        todo = f"{task['action']}: {task.get('working_directory', '')}/{task.get('filename', '')}"

                    message = Message.create_human_message(
                        step.implementation_prompt(
                            task=todo,
                            context=task["context"],
                        )
                    )
                    for output in self._graph.workflow.stream(
                        {"messages": [message]},
                        config={"recursion_limit": 50},
                    ):
                        for key, value in output.items():
                            yield value
                    count += 1
                    tasks["plan"].pop(0)

    def chat(self, message: str) -> None:
        for step in STEPS[self.step_type]:
            step = step(self.copilot, display=False, japanese_mode=self.japanese_mode)
            if step.__class__ is Specification:
                step.instructions = message
                step.app_type = self._("Client-Side Web Application")
            for agent in self.agents.to_array():
                agent.set_executor(step.working_directory)
            supervisor_name = (
                Chain()
                .create_assign_supervisor_chain(members=self.agents.to_array())
                .invoke(
                    {"messages": [Message.create_human_message(step.planning_prompt())]}
                )
                .get("assign")
            )
            supervisor = self.agents.get_agent_by_role(supervisor_name)
            self._graph = MultiAgentCollaborationGraph(
                supervisor, self.agents.to_array()
            )
            self.supervisor = supervisor
            tasks = (
                (
                    Chain()
                    .create_planning_chain(self.supervisor.profile)
                    .invoke(
                        {
                            "messages": [
                                Message.create_human_message(step.planning_prompt())
                            ],
                        }
                    )
                )
                if step.planning_prompt()
                else {"plan": []}
            )
            for task in step.additional_tasks():
                tasks["plan"].append(task)

            yield {
                "messages": [
                    Message.create_human_message(
                        message=str(tasks), name=self.supervisor.role.name
                    )
                ],
            }

            count = 1
            while len(tasks["plan"]) > 0:
                task = tasks["plan"][0]
                if task["action"] == ACTIONS[0]:
                    todo = f"{task['action']}: {task['command']} in the directory({task.get('working_directory', '')})"
                else:
                    todo = f"{task['action']}: {task.get('working_directory', '')}/{task.get('filename', '')}"

                message = Message.create_human_message(
                    step.implementation_prompt(
                        task=todo,
                        context=task["context"],
                    )
                )
                for output in self._graph.workflow.stream(
                    {"messages": [message]},
                    config={"recursion_limit": 50},
                ):
                    for key, value in output.items():
                        yield value
                count += 1
                tasks["plan"].pop(0)

    def improve(self, message: str) -> None:
        for step in STEPS[self.step_type]:
            step = step(self.copilot, display=False, japanese_mode=self.japanese_mode)
            step.improvement_request = message
            for agent in self.agents.to_array():
                agent.set_executor(step.working_directory)
            supervisor_name = (
                Chain()
                .create_assign_supervisor_chain(members=self.agents.to_array())
                .invoke(
                    {
                        "messages": [
                            Message.create_human_message(step.improvement_prompt())
                        ]
                    }
                )
                .get("assign")
            )
            supervisor = self.agents.get_agent_by_role(supervisor_name)
            self._graph = MultiAgentCollaborationGraph(
                supervisor, self.agents.to_array()
            )
            self.supervisor = supervisor
            tasks = (
                Chain()
                .create_planning_chain(self.supervisor.profile)
                .invoke(
                    {
                        "messages": [
                            Message.create_human_message(step.improvement_prompt())
                        ],
                    }
                )
            )

            yield {
                "messages": [
                    Message.create_human_message(
                        message=str(tasks), name=self.supervisor.role.name
                    )
                ],
            }

            count = 1
            while len(tasks["plan"]) > 0:
                task = tasks["plan"][0]
                if task["action"] == ACTIONS[0]:
                    todo = f"{task['action']}: {task['command']} in the directory({task.get('working_directory', '')})"
                else:
                    todo = f"{task['action']}: {task.get('working_directory', '')}/{task.get('filename', '')}"

                message = Message.create_human_message(
                    step.implementation_prompt(
                        task=todo,
                        context=task["context"],
                    )
                )
                for output in self._graph.workflow.stream(
                    {"messages": [message]},
                    config={"recursion_limit": 50},
                ):
                    for key, value in output.items():
                        yield value
                count += 1
                tasks["plan"].pop(0)
