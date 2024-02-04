from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.message import Message
from gpt_all_star.core.team import Team
from gpt_all_star.core.steps import step_prompts
from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.agents.engineer.implement_planning_prompt import (
    implement_planning_template,
)
from gpt_all_star.tool.text_parser import TextParser


class Development(Step):
    def __init__(
        self, agents: Agents, japanese_mode: bool, auto_mode: bool, debug_mode: bool
    ) -> None:
        super().__init__(agents, japanese_mode, auto_mode, debug_mode)

    def run(self) -> None:
        workflow = Team(
            supervisor=self.agents.copilot,
            members=[
                self.agents.engineer,
                self.agents.designer,
                self.agents.qa_engineer,
            ],
        )
        app = workflow.compile()

        todo_list = self.agents.engineer.plan_development(auto_mode=self.auto_mode)
        for i, task in enumerate(todo_list["plan"]):
            self.console.print(f"TODO {i + 1}: {task['todo']}")
            self.console.print(f"GOAL: {task['goal']}")
            self.console.print("---")

            current_contents = ""
            for (
                file_name,
                file_str,
            ) in self.agents.engineer.storages.root.recursive_file_search().items():
                if self.debug_mode:
                    self.console.print(
                        f"Adding file {file_name} to the prompt...", style="blue"
                    )
                code_input = step_prompts.format_file_to_input(file_name, file_str)
                current_contents += f"{code_input}\n"

            previous_finished_task_message = (
                "All preceding tasks have been completed. No further action is required on them.\n"
                + "All codes implemented so far are listed below. Please include them to ensure that we achieve our goal.\n"
                + f"{current_contents}\n\n"
                if i == 0
                else ""
            )
            message = Message.create_human_message(
                implement_planning_template.format(
                    todo_description=task["todo"],
                    finished_todo_message=previous_finished_task_message,
                    todo_goal=task["goal"],
                )
            )
            for output in app.stream({"messages": [message]}):
                for key, value in output.items():
                    self.console.print(f"Output from node '{key}':")
                    self.console.print("---")
                    if key == "copilot":
                        self.console.print(value)
                    else:
                        self.console.print(value.get("messages")[-1].content.strip())
                        files = TextParser.parse_code_from_text(
                            value.get("messages")[-1].content.strip()
                        )
                        for file_name, file_content in files:
                            self.agents.copilot.storages.root[file_name] = file_content
                print("\n---\n")

        self.agents.engineer.create_source_code(auto_mode=self.auto_mode)
        self.agents.engineer.complete_source_code(auto_mode=self.auto_mode)
        # self.console.new_lines()
        # self.agents.qa_engineer.evaluate_source_code(auto_mode=self.auto_mode)
        # self.console.new_lines()
