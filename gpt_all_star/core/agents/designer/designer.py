from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole
from gpt_all_star.core.agents.designer.design_user_interface_prompt import (
    design_user_interface_template,
)
from gpt_all_star.core.steps import step_prompts


class Designer(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str | None = None,
        profile: str | None = None,
    ) -> None:
        super().__init__(AgentRole.DESIGNER, storages, name, profile)

    def design_user_interface(self, auto_mode: bool = False):
        self.state("Okay, let's arrange the UI design!")
        self._console.new_lines()

        for file_name, file_str in self.storages.root.recursive_file_search().items():
            self._console.print(
                f"Adding file {file_name} to the prompt...", style="blue"
            )
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            self.messages.append(Message.create_system_message(f"{code_input}"))
        self._console.new_lines()

        self.messages.append(
            Message.create_system_message(
                design_user_interface_template.format(
                    specifications=self.storages.docs["specifications.md"]
                )
            )
        )

        self.chat()

        files = Message.parse_message(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.root[file_name] = file_content
