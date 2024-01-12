from enum import Enum

from your_dev_team.core.steps.Development import Development
from your_dev_team.core.steps.Execution import Execution
from your_dev_team.core.steps.Specification import Specification
from your_dev_team.core.steps.SystemDesign import SystemDesign
from your_dev_team.core.steps.TeamBuilding import TeamBuilding


class StepType(str, Enum):
    DEFAULT = "default"
    TEAM_BUILDING = "team_building"
    SPECIFICATION = "specification"
    SYSTEM_DESIGN = "system_design"
    DEVELOPMENT = "development"
    EXECUTION = "execution"


STEPS = {
    StepType.DEFAULT: [
        TeamBuilding,
        Specification,
        SystemDesign,
        Development,
        Execution,
    ],
    StepType.TEAM_BUILDING: [TeamBuilding],
    StepType.SPECIFICATION: [Specification],
    StepType.SYSTEM_DESIGN: [SystemDesign],
    StepType.DEVELOPMENT: [Development],
    StepType.EXECUTION: [Execution],
}
