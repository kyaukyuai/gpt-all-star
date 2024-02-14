from enum import Enum

from gpt_all_star.core.steps.deployment.deployment import Deployment
from gpt_all_star.core.steps.development.development import Development
from gpt_all_star.core.steps.execution import Execution
from gpt_all_star.core.steps.improvement.improvement import Improvement
from gpt_all_star.core.steps.specification.specification import Specification
from gpt_all_star.core.steps.system_design import SystemDesign
from gpt_all_star.core.steps.team_building.team_building import TeamBuilding
from gpt_all_star.core.steps.ui_design.ui_design import UIDesign


class StepType(str, Enum):
    DEFAULT = "default"
    """Represents the default step type."""
    BUILD = "build"
    """Represents the build step type."""
    TEAM_BUILDING = "team_building"
    """Represents the team building step type."""
    SPECIFICATION = "specification"
    """Represents the specification step type."""
    SYSTEM_DESIGN = "system_design"
    """Represents the system design step type."""
    DEVELOPMENT = "development"
    """Represents the development step type."""
    UI_DESIGN = "ui_design"
    """Represents the UI design step type."""
    EXECUTION = "execution"
    """Represents the execution step type."""
    IMPROVEMENT = "improvement"
    """Represents the improvement step type."""
    DEPLOYMENT = "deployment"
    """Represents the deployment step type."""


"""Enum representing different step types."""

STEPS = {
    StepType.DEFAULT: [
        TeamBuilding,
        Specification,
        SystemDesign,
        Development,
        UIDesign,
        Execution,
        Deployment,
    ],
    StepType.BUILD: [
        Development,
        UIDesign,
        Execution,
        Deployment,
    ],
    StepType.TEAM_BUILDING: [TeamBuilding],
    StepType.SPECIFICATION: [Specification],
    StepType.SYSTEM_DESIGN: [SystemDesign],
    StepType.DEVELOPMENT: [Development],
    StepType.UI_DESIGN: [UIDesign],
    StepType.EXECUTION: [Execution],
    StepType.IMPROVEMENT: [Improvement],
    StepType.DEPLOYMENT: [Deployment],
}
