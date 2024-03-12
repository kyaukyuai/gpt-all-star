from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.steps.improvement.planning_prompt import planning_prompt_template
from gpt_all_star.core.steps.step import Step
from gpt_all_star.helper.translator import create_translator


class Improvement(Step):
    def __init__(
            self,
            copilot: Copilot,
            display: bool = True,
            japanese_mode: bool = False
    ) -> None:
        super().__init__(copilot, display)
        self.working_directory = self.copilot.storages.app.path.absolute()
        self._ = create_translator('ja' if japanese_mode else 'en')

    def planning_prompt(self) -> str:
        request = self.copilot.ask(
            self._("What would you like to update?"), is_required=True, default=None
        )
        planning_prompt = planning_prompt_template.format(
            request=request,
            current_source_code=self.copilot.storages.current_source_code(
                debug_mode=self.copilot.debug_mode
            ),
        )
        return planning_prompt

    def additional_tasks(self) -> list:
        return []

    def callback(self) -> bool:
        self.copilot.output_files(exclude_dirs=self.exclude_dirs)
        return True
