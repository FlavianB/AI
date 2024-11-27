
from enum import Enum
from returns.result import Result, Success, Failure

class Weight(Enum):
    HARD= 'hard'
    SOFT= 'soft'
    SOFTHARD = 'softhard'

    @staticmethod
    def from_string(value: str) -> Result['Weight', str]:
        try:
            return Success(Weight(value))
        except ValueError:
            return Failure(f"Invalid weight '{value}'.\n")

class ConstraintType(Enum):
    STAFF_UNAVAILABLE = "unavailable_staff_time"
    CLASSROOM_UNAVAILABLE = "unavailable_classroom_time"
    PREFERRED_EVENT = "preferred_event"