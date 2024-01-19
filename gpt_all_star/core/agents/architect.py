from gpt_all_star.core.message import Message
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.agents.agent import Agent, AgentRole, NEXT_COMMAND
from gpt_all_star.core.steps import step_prompts


class Architect(Agent):
    def __init__(
        self,
        storages: Storages,
        name: str = "architect",
        profile: str = AgentRole.default_profile()[AgentRole.ARCHITECT].format(),
    ) -> None:
        super().__init__(AgentRole.ARCHITECT, storages, name, profile)

    def plan(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.design_systems_planning_template.format(
                    specifications=self.storages.docs["specifications.md"]
                )
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

    def list_technology_stack(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.design_systems_template.format(
                    specifications=self.storages.docs["specifications.md"]
                )
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs["technology_stack.md"] = file[1]
        self.state("Here are the technology stack:")
        self.output_md(self.storages.docs["technology_stack.md"])

    def layout_directory(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.layout_directory_template.format(
                    specifications=self.storages.docs["specifications.md"],
                    technology_stack=self.storages.docs["technology_stack.md"],
                )
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND
            ),
        )

        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs["layout_directory.md"] = file[1]
        self.state("Here are the layout directory:")
        self.output_md(self.storages.docs["layout_directory.md"])
