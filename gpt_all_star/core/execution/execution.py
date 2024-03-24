from gpt_all_star.core.agents.chain import Chain
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.message import Message
from gpt_all_star.core.steps.healing.healing import Healing
from gpt_all_star.core.team import Team
from gpt_all_star.helper.translator import create_translator


class Execution:
    def __init__(self, team: Team, copilot: Copilot, japanese_mode: bool) -> None:
        self.team = team
        self.copilot = copilot
        self.working_directory = self.copilot.storages.app.path.absolute()
        self._ = create_translator("ja" if japanese_mode else "en")

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
        self.copilot.caution(command["command"])
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.copilot.state(self._("Attempt %d/%d") % (attempt + 1, MAX_ATTEMPTS))
            try:
                self.copilot.run_command(command["command"])
                return
            except KeyboardInterrupt:
                break
            except Exception as e:
                healing = Healing(copilot=self.copilot, error_message=e)
                self.team.run(healing)
