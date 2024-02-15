from enum import Enum

from gpt_all_star.core.steps.deployment.deployment import Deployment
from gpt_all_star.core.steps.development.development import Development
from gpt_all_star.core.steps.execution.execution import Execution
from gpt_all_star.core.steps.improvement.improvement import Improvement
from gpt_all_star.core.steps.specification.specification import Specification
from gpt_all_star.core.steps.system_design.system_design import SystemDesign
from gpt_all_star.core.steps.team_building.team_building import TeamBuilding
from gpt_all_star.core.steps.ui_design.ui_design import UIDesign


class StepType(str, Enum):
    """
    Represents the type of step in the development process.

    This enum class specifies the different types of steps available in the development process.
    It provides a clear and concise enumeration of the step types, which can be used to categorize and identify different steps.

    Usage:
    Use this enum to define the step type for each phase of the development process.
    """
    DEFAULT = "default"
    BUILD = "build"
    TEAM_BUILDING = "team_building"
    SPECIFICATION = "specification"
    SYSTEM_DESIGN = "system_design"
    DEVELOPMENT = "development"
    UI_DESIGN = "ui_design"
    EXECUTION = "execution"
    IMPROVEMENT = "improvement"
    DEPLOYMENT = "deployment"


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
