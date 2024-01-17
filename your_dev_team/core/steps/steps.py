from enum import Enum

from your_dev_team.core.steps.deployment import Deployment
from your_dev_team.core.steps.development import Development
from your_dev_team.core.steps.execution import Execution
from your_dev_team.core.steps.improvement import Improvement
from your_dev_team.core.steps.specification import Specification
from your_dev_team.core.steps.system_design import SystemDesign
from your_dev_team.core.steps.team_building import TeamBuilding


class StepType(str, Enum):
    DEFAULT = "default"
    TEAM_BUILDING = "team_building"
    SPECIFICATION = "specification"
    SYSTEM_DESIGN = "system_design"
    DEVELOPMENT = "development"
    EXECUTION = "execution"
    IMPROVEMENT = "improvement"
    DEPLOYMENT = "deployment"


STEPS = {
    StepType.DEFAULT: [
        TeamBuilding,
        Specification,
        SystemDesign,
        Development,
        Execution,
        Improvement,
        Deployment,
    ],
    StepType.TEAM_BUILDING: [TeamBuilding],
    StepType.SPECIFICATION: [Specification],
    StepType.SYSTEM_DESIGN: [SystemDesign],
    StepType.DEVELOPMENT: [Development],
    StepType.EXECUTION: [Execution],
    StepType.IMPROVEMENT: [Improvement],
    StepType.DEPLOYMENT: [Deployment],
}
