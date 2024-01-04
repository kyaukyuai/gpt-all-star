from enum import Enum

from core.steps.Development import Development
from core.steps.Execution import Execution
from core.steps.Specification import Specification


class StepType(str, Enum):
    DEFAULT = "default"
    SPECIFICATION = "specification"
    DEVELOPMENT = "development"
    EXECUTION = "execution"


STEPS = {
    StepType.DEFAULT: [Specification, Development, Execution],
    StepType.SPECIFICATION: [Specification],
    StepType.DEVELOPMENT: [Development],
    StepType.EXECUTION: [Execution],
}
