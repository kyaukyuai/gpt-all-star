from enum import Enum

from core.steps.Clarify import Clarify
from core.steps.Development import Development
from core.steps.Specification import Specification


class StepType(str, Enum):
    DEFAULT = "default"


STEPS = {
    StepType.DEFAULT: [Clarify, Specification, Development]
}
