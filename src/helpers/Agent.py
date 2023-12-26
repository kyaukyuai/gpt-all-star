from pprint import pprint


class Agent:
    def __init__(self, role: str, project) -> None:
        """
        Agent constructor

        :param role: Role of this agent
        :param project: Project of this agent
        """
        from helpers.Project import Project

        if not isinstance(role, str) or not role:
            raise ValueError("`role` should be a non-empty string")
        if not isinstance(project, Project):
            raise ValueError("`project` should be an instance of Project")

        self.role: str = role
        self.project: Project = project

    def print_role(self) -> None:
        """
        Prints the role of this agent
        """
        pprint(f'The role of this agent is {self.role}')

    def print_project(self) -> None:
        """
        Prints the project of this agent
        """
        pprint(f'The project of this agent is {self.project.name}')
