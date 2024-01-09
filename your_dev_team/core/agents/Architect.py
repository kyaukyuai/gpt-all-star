from your_dev_team.core.Message import Message
from your_dev_team.core.Storage import Storages
from your_dev_team.core.agents.Agent import Agent, AgentRole, NEXT_COMMAND
from your_dev_team.core.steps import step_prompts


class Architect(Agent):
    def __init__(self, storages: Storages) -> None:
        super().__init__(AgentRole.ARCHITECT, storages)

    def list_technology_stack(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.design_systems_template.format(specifications=self.storages.docs['specifications.md'])
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND),
        )

        self.storages.memory['technology_stack'] = Message.serialize_messages(self.messages)
        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs['technology_stack.md'] = file[1]

    def layout_directory(self):
        self.messages.append(
            Message.create_system_message(
                step_prompts.layout_directory_template.format(
                    specifications=self.storages.docs['specifications.md'],
                    technology_stack=self.storages.docs['technology_stack.md']
                )
            )
        )

        self._execute(
            "Do you want to add any features or changes? If yes, describe it here and if no, just type `{}`".format(
                NEXT_COMMAND),
        )

        self.storages.memory['layout_directory'] = Message.serialize_messages(self.messages)
        file = Message.parse_message(self.latest_message_content())[0]
        self.storages.docs['layout_directory.md'] = file[1]
