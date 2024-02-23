import unittest

from gpt_all_star.core.steps.entrypoint.entrypoint import Entrypoint
from gpt_all_star.core.steps.steps import STEPS, StepType
from gpt_all_star.core.steps.ui_design.ui_design import UIDesign


class TestSteps(unittest.TestCase):
    def test_step_type_enum(self):
        self.assertEqual(StepType.UI_DESIGN, "ui_design")
        self.assertEqual(StepType.ENTRYPOINT, "entrypoint")

    def test_steps_dictionary(self):
        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.DEFAULT])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.DEFAULT])
        self.assertIn(UIDesign, STEPS[StepType.DEFAULT])
        self.assertIn(Entrypoint, STEPS[StepType.DEFAULT])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.BUILD])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.BUILD])
        self.assertIn(UIDesign, STEPS[StepType.BUILD])
        self.assertIn(Entrypoint, STEPS[StepType.BUILD])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.DEFAULT])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.DEFAULT])
        self.assertIn(UIDesign, STEPS[StepType.DEFAULT])
        self.assertIn(Entrypoint, STEPS[StepType.DEFAULT])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.SPECIFICATION])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.SPECIFICATION])
        self.assertIn(UIDesign, STEPS[StepType.SPECIFICATION])
        self.assertIn(Entrypoint, STEPS[StepType.SPECIFICATION])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.SYSTEM_DESIGN])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.SYSTEM_DESIGN])
        self.assertIn(UIDesign, STEPS[StepType.SYSTEM_DESIGN])
        self.assertIn(Entrypoint, STEPS[StepType.SYSTEM_DESIGN])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.DEVELOPMENT])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.DEVELOPMENT])
        self.assertIn(UIDesign, STEPS[StepType.DEVELOPMENT])
        self.assertIn(Entrypoint, STEPS[StepType.DEVELOPMENT])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.ENTRYPOINT])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.ENTRYPOINT])
        self.assertIn(UIDesign, STEPS[StepType.ENTRYPOINT])
        self.assertIn(Entrypoint, STEPS[StepType.ENTRYPOINT])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.UI_DESIGN])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.UI_DESIGN])
        self.assertIn(UIDesign, STEPS[StepType.UI_DESIGN])
        self.assertIn(Entrypoint, STEPS[StepType.UI_DESIGN])

        self.assertIn(StepType.UI_DESIGN, STEPS[StepType.IMPROVEMENT])
        self.assertIn(StepType.ENTRYPOINT, STEPS[StepType.IMPROVEMENT])
        self.assertIn(UIDesign, STEPS[StepType.IMPROVEMENT])
        self.assertIn(Entrypoint, STEPS[StepType.IMPROVEMENT])

if __name__ == '__main__':
    unittest.main()
