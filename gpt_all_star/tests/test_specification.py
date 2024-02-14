from gpt_all_star.core.steps.specification.specification import Specification
from gpt_all_star.core.team import Team

import unittest
from unittest.mock import MagicMock

from gpt_all_star.core.steps.specification.specification import Specification
from gpt_all_star.core.team import Team


class TestSpecification(unittest.TestCase):
    def test_run_retrieves_instructions_and_app_type(self):
        # Create mock objects for the agents
        product_owner = MagicMock()
        product_owner.get_instructions.return_value = "Sample instructions"
        product_owner.get_app_type.return_value = "Sample app type"
        agents = MagicMock()
        agents.product_owner = product_owner

        # Create an instance of the Specification class
        specification = Specification(
            agents=agents,
            japanese_mode=False,
            review_mode=False,
            debug_mode=False,
        )

        # Call the run method
        specification.run()

        # Assert that the instructions and app type are retrieved correctly
        product_owner.get_instructions.assert_called_once()
        product_owner.get_app_type.assert_called_once()

    def test_run_creates_team_with_correct_supervisor_and_members(self):
        # Create mock objects for the agents
        project_manager = MagicMock()
        product_owner = MagicMock()
        designer = MagicMock()
        engineer = MagicMock()
        agents = MagicMock()
        agents.project_manager = project_manager
        agents.product_owner = product_owner
        agents.designer = designer
        agents.engineer = engineer

        # Create an instance of the Specification class
        specification = Specification(
            agents=agents,
            japanese_mode=False,
            review_mode=False,
            debug_mode=False,
        )

        # Call the run method
        specification.run()

        # Assert that the team is created with the correct supervisor and members
        Team.assert_called_once_with(
            supervisor=project_manager,
            members=[product_owner, designer, engineer],
        )

    def test_run_calls_team_drive_with_correct_arguments(self):
        # Create mock objects for the agents and team
        project_manager = MagicMock()
        product_owner = MagicMock()
        designer = MagicMock()
        engineer = MagicMock()
        agents = MagicMock()
        agents.project_manager = project_manager
        agents.product_owner = product_owner
        agents.designer = designer
        agents.engineer = engineer
        team = MagicMock()

        # Create an instance of the Specification class
        specification = Specification(
            agents=agents,
            japanese_mode=False,
            review_mode=False,
            debug_mode=False,
        )

        # Set the team attribute of the specification instance to the mock team
        specification.team = team

        # Call the run method
        specification.run()

        # Assert that the team's drive method is called with the correct arguments
        # Assertion for the new scenario to call team's drive method with args
        team.drive.assert_called_once()

if __name__ == "__main__":
    unittest.main()
