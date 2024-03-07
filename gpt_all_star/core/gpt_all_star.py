from gpt_all_star.core.project import Project
from gpt_all_star.core.steps.steps import StepType


class GptAllStar:
    def __init__(self):
        pass

    def chat(self, project_name: str, step: StepType = None, message=None):
        project = Project(step=step, project_name=project_name)
        return project.chat(message=message)
