from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.execution.planning_prompt import planning_prompt_template
from gpt_all_star.core.storage import Storages
from gpt_all_star.core.team import Team


class Execution:
    def __init__(
        self,
        team: Team,
        storages: Storages,
        agents: Agents,
        japanese_mode: bool,
        review_mode: bool,
        debug_mode: bool,
    ) -> None:
        self.team = team
        self.storages = storages
        self.agents = agents
        self.japanese_mode = japanese_mode
        self.review_mode = review_mode
        self.debug_mode = debug_mode

    def run(self) -> None:
        self.agents.qa_engineer.confirm_execution(
            review_mode=self.review_mode,
            command=self.agents.qa_engineer.storages.root["./app/run.sh"],
        )
        MAX_ATTEMPTS = 5
        for attempt in range(MAX_ATTEMPTS):
            self.agents.qa_engineer.state(f"Attempt {attempt + 1}/{MAX_ATTEMPTS}")
            try:
                self.agents.qa_engineer.run_command()
            except KeyboardInterrupt:
                break
            except Exception as e:
                planning_prompt = planning_prompt_template.format(
                    error=e,
                    current_source_code=self.storages.current_source_code(),
                )
                self.team.drive(planning_prompt)
