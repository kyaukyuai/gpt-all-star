from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.execution.planning_prompt import planning_prompt_template
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.team import Team


class Execution:
    def __init__(
        self,
        team: Team,
        storages: Storages,
        copilot: Copilot,
        agents: Agents,
    ) -> None:
        self.team = team
        self.storages = storages
        self.copilot = copilot
        self.agents = agents

    def run(self) -> None:
        self.copilot.caution()
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.copilot.state(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}")
            try:
                self.agents.qa_engineer.run_command()
            except KeyboardInterrupt:
                break
            except Exception as e:
                planning_prompt = planning_prompt_template.format(
                    error=e,
                    current_source_code=self.storages.current_source_code(),
                )
                self.team.run(planning_prompt)
