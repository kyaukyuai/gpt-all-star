from pprint import pprint


class Project:
    def __init__(self, args, name=None, description=None, user_stories=None, user_tasks=None, architecture=None,
                 development_plan=None, current_step=None):
        self.args = args
        self.current_step = current_step
        self.name = name
        self.description = description
        self.user_stories = user_stories
        self.user_tasks = user_tasks
        self.architecture = architecture
        self.development_plan = development_plan

        self._print_settings()

    def _print_settings(self):
        pprint(
            f"Project setting is set with args: {self.args},"
            f"name: {self.name}, description: {self.description}, user_stories: {self.user_stories},"
            f"user_tasks: {self.user_tasks}, architecture: {self.architecture},"
            f"development_plan: {self.development_plan}, current_step: {self.current_step}")
