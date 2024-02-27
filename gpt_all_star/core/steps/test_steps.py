import unittest

from gpt_all_star.core.steps.steps import StepType


class TestSteps(unittest.TestCase):
    def test_step_type_none(self):
        self.assertEqual(StepType.NONE, "none")

    def test_step_type_default(self):
        self.assertEqual(StepType.DEFAULT, "default")

    def test_step_type_build(self):
        self.assertEqual(StepType.BUILD, "build")

    def test_step_type_specification(self):
        self.assertEqual(StepType.SPECIFICATION, "specification")

    def test_step_type_system_design(self):
        self.assertEqual(StepType.SYSTEM_DESIGN, "system_design")

    def test_step_type_development(self):
        self.assertEqual(StepType.DEVELOPMENT, "development")

    def test_step_type_entrypoint(self):
        self.assertEqual(StepType.ENTRYPOINT, "entrypoint")

    def test_step_type_ui_design(self):
        self.assertEqual(StepType.UI_DESIGN, "ui_design")

    def test_step_type_improvement(self):
        self.assertEqual(StepType.IMPROVEMENT, "improvement")

    def test_step_type_healing(self):
        self.assertEqual(StepType.HEALING, "healing")


if __name__ == "__main__":
    unittest.main()
