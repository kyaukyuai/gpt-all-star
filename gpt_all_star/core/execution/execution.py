from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.execution.planning_prompt import planning_prompt_template
from gpt_all_star.core.team import Team


class Execution:
    def __init__(
        self,
        team: Team,
        copilot: Copilot,
    ) -> None:
        self.team = team
        self.copilot = copilot
        self.working_directory = self.copilot.storages.app.path.absolute()

    def run(self) -> None:
        self.copilot.caution()
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.copilot.state(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}")
            try:
                self.copilot.run_command()
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
