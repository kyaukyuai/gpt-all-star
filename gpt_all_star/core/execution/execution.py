from gpt_all_star.core.agents.chain import Chain
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.execution.planning_prompt import planning_prompt_template
from gpt_all_star.core.message import Message
from gpt_all_star.core.team import Team


class Execution:
    """
    Class representing the execution of the application.

    Attributes:
        team (Team): The team object.
        copilot (Copilot): The copilot object.
        working_directory (str): The absolute path of the working directory.
    """
    def __init__(
        self,
        team: Team,
        copilot: Copilot,
    ) -> None:
        """
        Initialize the Execution object.

        Args:
            team (Team): The team object.
            copilot (Copilot): The copilot object.
        """
        self.team = team
        self.copilot = copilot
        self.working_directory = self.copilot.storages.app.path.absolute()

    def run(self) -> None:
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
- If run.sh exists, use it in preference.

# Current Implementation
---
{self.copilot.storages.current_source_code()}
"""
                        )
                    ],
                }
            )
        )
        self.copilot.caution(command["command"])
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.copilot.state(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}")
            try:
                self.copilot.run_command(command["command"])
            except KeyboardInterrupt:
                break
            except Exception as e:
                planning_prompt = planning_prompt_template.format(
                    error=e,
                    current_source_code=self.copilot.storages.current_source_code(),
                )
                for agent in self.team.agents.to_array():
                    agent.set_executor(self.working_directory)
                self.team._run(planning_prompt)
                break
            except Exception as e:
                planning_prompt = planning_prompt_template.format(
                    error=e,
                    current_source_code=self.copilot.storages.current_source_code(),
                )
                for agent in self.team.agents.to_array():
                    agent.set_executor(self.working_directory)
                self.team._run(planning_prompt)
