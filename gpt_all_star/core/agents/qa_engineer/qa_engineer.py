from __future__ import annotations

from gpt_all_star.core.message import Message
from gpt_all_star.core.steps import step_prompts
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.qa_engineer.analyze_source_code_prompt import (
    analyze_source_code_template,
)


class QAEngineer(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.QA_ENGINEER, storages, name, profile)

    def analyze_source_code(self, auto_mode: bool = False):
        self.state("Okay, let's analyze the code!")
        self.console.new_lines()

        for file_name, file_str in self.storages.root.recursive_file_search().items():
            self.console.print(
                f"Adding file {file_name} to the prompt...", style="blue"
            )
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            self.messages.append(Message.create_system_message(f"{code_input}"))
        self.console.new_lines()

        self.messages.append(
            Message.create_system_message(analyze_source_code_template.format())
        )

        self.chat()

        files = Message.parse_message(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.root[file_name] = file_content
