from enum import Enum

from gpt_all_star.core.steps.deployment import Deployment
from gpt_all_star.core.steps.development import Development
from gpt_all_star.core.steps.execution import Execution
from gpt_all_star.core.steps.improvement import Improvement
from gpt_all_star.core.steps.specification import Specification
from gpt_all_star.core.steps.system_design import SystemDesign
from gpt_all_star.core.steps.team_building import TeamBuilding
from gpt_all_star.core.steps.ui_design import UIDesign


class StepType(str, Enum):
    DEFAULT = "default"
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
        Improvement,
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
