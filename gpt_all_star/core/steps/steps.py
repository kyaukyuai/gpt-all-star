from enum import Enum

from gpt_all_star.core.steps.development.development import Development
from gpt_all_star.core.steps.entrypoint.entrypoint import Entrypoint
from gpt_all_star.core.steps.improvement.improvement import Improvement
from gpt_all_star.core.steps.specification.specification import Specification
from gpt_all_star.core.steps.system_design.system_design import SystemDesign
from gpt_all_star.core.steps.ui_design.ui_design import UIDesign


class StepType(str, Enum):
    NONE = "none"
    DEFAULT = "default"
    BUILD = "build"
    SPECIFICATION = "specification"
    SYSTEM_DESIGN = "system_design"
    DEVELOPMENT = "development"
    ENTRYPOINT = "entrypoint"
    UI_DESIGN = "ui_design"
    IMPROVEMENT = "improvement"


STEPS = {
    StepType.NONE: [],
    StepType.DEFAULT: [
        Specification,
        SystemDesign,
        Development,
        UIDesign,
        Entrypoint,
    ],
    StepType.BUILD: [
        Development,
        UIDesign,
        Entrypoint,
    ],
    StepType.SPECIFICATION: [Specification],
    StepType.SYSTEM_DESIGN: [SystemDesign],
    StepType.DEVELOPMENT: [Development],
    StepType.ENTRYPOINT: [Entrypoint],
    StepType.UI_DESIGN: [UIDesign],
    StepType.IMPROVEMENT: [Improvement],
}
