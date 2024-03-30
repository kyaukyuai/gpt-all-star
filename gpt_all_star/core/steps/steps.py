from enum import Enum

from gpt_all_star.core.steps.development.development import Development
from gpt_all_star.core.steps.entrypoint.entrypoint import Entrypoint
from gpt_all_star.core.steps.healing.healing import Healing
from gpt_all_star.core.steps.specification.specification import Specification
from gpt_all_star.core.steps.system_design.system_design import SystemDesign
from gpt_all_star.core.steps.ui_design.ui_design import UIDesign
from gpt_all_star.core.steps.ui_development.ui_development import UIDevelopment


class StepType(str, Enum):
    NONE = "none"
    DEFAULT = "default"
    BUILD = "build"
    SPECIFICATION = "specification"
    SYSTEM_DESIGN = "system_design"
    DEVELOPMENT = "development"
    UI_DEVELOPMENT = "ui_development"
    ENTRYPOINT = "entrypoint"
    UI_DESIGN = "ui_design"
    HEALING = "healing"


STEPS = {
    StepType.NONE: [],
    StepType.DEFAULT: [
        Specification,
        SystemDesign,
        UIDesign,
        Development,
        UIDevelopment,
        Entrypoint,
    ],
    StepType.BUILD: [
        Development,
        UIDevelopment,
        Entrypoint,
    ],
    StepType.SPECIFICATION: [Specification],
    StepType.SYSTEM_DESIGN: [SystemDesign],
    StepType.DEVELOPMENT: [Development],
    StepType.UI_DEVELOPMENT: [UIDevelopment],
    StepType.ENTRYPOINT: [Entrypoint],
    StepType.UI_DESIGN: [UIDesign],
    StepType.HEALING: [Healing],
}
