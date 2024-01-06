from enum import Enum

from core.steps.Development import Development
from core.steps.Execution import Execution
from core.steps.Specification import Specification
from core.steps.SystemDesign import SystemDesign


class StepType(str, Enum):
    DEFAULT = "default"
    SPECIFICATION = "specification"
    SYSTEM_DESIGN = "system_design"
    DEVELOPMENT = "development"
    EXECUTION = "execution"


STEPS = {
    StepType.DEFAULT: [Specification, SystemDesign, Development, Execution],
    StepType.SPECIFICATION: [Specification],
    StepType.SYSTEM_DESIGN: [SystemDesign],
    StepType.DEVELOPMENT: [Development],
    StepType.EXECUTION: [Execution],
}
