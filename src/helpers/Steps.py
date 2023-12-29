from enum import Enum

from helpers.steps.Clarify import Clarify
from helpers.steps.Specification import Specification


class StepType(str, Enum):
    DEFAULT = "default"


STEPS = {
    StepType.DEFAULT: [Clarify, Specification]
}
