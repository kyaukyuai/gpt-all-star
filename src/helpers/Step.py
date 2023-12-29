from enum import Enum

from helpers.Message import Message


class Step:
    def __init__(self) -> None:
        self.conversation = Message()


class StepType(str, Enum):
    DEFAULT = "default"


STEPS = {
    StepType.DEFAULT: ['clarify', 'update_specification']
}
