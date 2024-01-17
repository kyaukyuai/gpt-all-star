from your_dev_team.core.message import Message
from your_dev_team.core.storage import Storages
from your_dev_team.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from your_dev_team.core.steps import step_prompts


class Designer(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str = "designer",
        profile: str = AgentRole.default_profile()[AgentRole.DESIGNER].format(),
    ) -> None:
        super().__init__(AgentRole.DESIGNER, storages, name, profile)

    def arrange_ui_design(self):
        self.state("Okay, let's arrange the UI design!")
        self._console.new_lines(1)

        for file_name, file_str in self._get_code_strings().items():
            self._console.print(
                f"Adding file {file_name} to the prompt...", style="blue"
            )
            code_input = step_prompts.format_file_to_input(file_name, file_str)
            self.messages.append(Message.create_system_message(f"{code_input}"))

        self.messages.append(
            Message.create_system_message(
                step_prompts.arrange_ui_design_template.format()
            )
        )

        self.chat()

        files = Message.parse_message(self.latest_message_content())
        for file_name, file_content in files:
            self.storages.origin[file_name] = file_content

    def _get_code_strings(self) -> dict[str, str]:
        return self.storages.origin.recursive_file_search()
