import unittest
from unittest.mock import MagicMock

from gpt_all_star.core.steps.step import Step
from gpt_all_star.core.steps.team_building import Team
from gpt_all_star.core.steps.ui_design.ui_design import UIDesign


class TestUIDesign(unittest.TestCase):
    def test_initialization(self):
        agents = MagicMock()
        japanese_mode = False
        review_mode = False
        debug_mode = False

        ui_design = UIDesign(agents, japanese_mode, review_mode, debug_mode)

        self.assertIsInstance(ui_design, Step)
        self.assertEqual(ui_design.agents, agents)
        self.assertEqual(ui_design.japanese_mode, japanese_mode)
        self.assertEqual(ui_design.review_mode, review_mode)
        self.assertEqual(ui_design.debug_mode, debug_mode)

    def test_run(self):
        agents = MagicMock()
        japanese_mode = False
        review_mode = False
        debug_mode = False

        team = MagicMock(spec=Team)
        team.supervisor.current_source_code.return_value = "source_code"
        team.supervisor.storages.docs.__getitem__.return_value = "specifications.md"

        agents.project_manager = MagicMock()
        agents.engineer = MagicMock()
        agents.designer = MagicMock()
        agents.qa_engineer = MagicMock()

        ui_design = UIDesign(agents, japanese_mode, review_mode, debug_mode)
        ui_design.run()

        team.supervisor.current_source_code.assert_called_once()
        team.supervisor.storages.docs.__getitem__.assert_called_once_with("specifications.md")
        team.drive.assert_called_once_with(
            f"source_code\nspecifications.md"
        )


if __name__ == "__main__":
    unittest.main()
