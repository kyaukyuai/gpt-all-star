from enum import Enum

from core.steps.Clarify import Clarify
from core.steps.Development import Development
from core.steps.Execution import Execution
from core.steps.Specification import Specification


class StepType(str, Enum):
    DEFAULT = "default"
    CLARIFY = "clarify"
    SPECIFICATION = "specification"
    DEVELOPMENT = "development"
    EXECUTION = "execution"


STEPS = {
    StepType.DEFAULT: [Clarify, Specification, Development, Execution],
    StepType.CLARIFY: [Clarify],
    StepType.SPECIFICATION: [Specification],
    StepType.DEVELOPMENT: [Development],
    StepType.EXECUTION: [Execution],
}
