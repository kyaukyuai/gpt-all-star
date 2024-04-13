from gpt_all_star.core.respond import Respond
from gpt_all_star.core.steps.steps import StepType


class GptAllStar:
    def __init__(self):
        pass

    def chat(
        self,
        project_name: str,
        step: StepType = None,
        message=None,
        japanese_mode: bool = False,
    ):
        respond = Respond(
            step=step, project_name=project_name, japanese_mode=japanese_mode
        )
        return respond.chat(message=message)

    def improve(
        self,
        project_name: str,
        step: StepType = None,
        message=None,
        japanese_mode: bool = False,
    ):
        respond = Respond(
            step=step, project_name=project_name, japanese_mode=japanese_mode
        )
        return respond.improve(message=message)

    def execute(self, project_name: str, japanese_mode: bool = False):
        respond = Respond(
            step=StepType.NONE, project_name=project_name, japanese_mode=japanese_mode
        )
        return respond.execute()

    def deploy(self, project_name: str, japanese_mode: bool = False):
        respond = Respond(
            step=StepType.NONE, project_name=project_name, japanese_mode=japanese_mode
        )
        return respond.deploy()
