import json
from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.team import Team
from gpt_all_star.core.implement_planning_prompt import (
    implement_planning_template,
)


class Execution(Step):
    def __init__(
        self,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        super().__init__(agents, japanese_mode, review_mode, debug_mode)

    def run(self) -> None:
        from gpt_all_star.core.steps.improvement import Improvement

        self.agents.qa_engineer.confirm_execution(
            review_mode=self.review_mode,
            command=self.agents.qa_engineer.storages.root["run.sh"],
        )
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.agents.qa_engineer.state(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}")
            try:
                self.agents.qa_engineer.run_command()
            except KeyboardInterrupt:
                break
            except Exception as e:
                team = Team(
                    supervisor=self.agents.project_manager,
                    members=[
                        self.agents.engineer,
                        self.agents.designer,
                        self.agents.qa_engineer,
                    ],
                )
                todo_list = self.agents.project_manager.create_planning_chain().invoke(
                    {
                        "messages": [
                            Message.create_human_message(
                                f"""
    # Instructions
    ---
    Create a detailed and specific development plan to rectify the following errors.

    # Constraints
    ---
    Understand the exact error wording and be sure to correct it.

    ## Error
    ```
    {e}
    ```

    # Current implementation
    ---
    ```
    {self.agents.project_manager.current_source_code()}
    ```
    """
                            )
                        ],
                    },
                )

            print(json.dumps(todo_list, indent=4))

            for i, task in enumerate(todo_list["plan"]):
                team.supervisor.state(
                    f"""\n
    Task {i + 1}: {task['task']}
    Objective: {task['objective']}
    Reason: {task['reason']}
    ---
    """
                )

                if task["task"] == "executing a command":
                    todo = f"{task['task']}: {task['command']} in the directory {task['working_directory']}"
                else:
                    todo = f"{task['task']}: {task['working_directory']}/{task['filename']}"
                message = Message.create_human_message(
                    implement_planning_template.format(
                        task=todo,
                        objective=task["objective"],
                        context=task["context"],
                        reason=task["reason"],
                        implementation=self.agents.project_manager.current_source_code(),
                        specifications=self.agents.project_manager.storages.docs[
                            "specifications.md"
                        ],
                    )
                )
                team.run([message])

        CONFIRM_CHOICES = ["yes", "no"]
        choice = self.agents.copilot.present_choices(
            "Do you want to improve your source code again?",
            CONFIRM_CHOICES,
            default=1,
        )
        if choice == CONFIRM_CHOICES[0]:
            Improvement(
                self.agents, self.japanese_mode, self.review_mode, self.debug_mode
            ).run()
