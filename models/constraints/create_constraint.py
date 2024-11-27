from typing import Any, Dict
from models.constraints.constants import ConstraintType, Weight
from models.constraints.constraint import Constraint
from models.constraints.preffered_event import PreferredEvent
from models.constraints.unavailable_classroom_time import UnavailableClassroomTime
from models.constraints.unavailable_staff_time import UnavailableStaffTime
from returns.result import Result, Failure, Success
from returns.pipeline import is_successful

def create_constraint(data: Dict[str, Any]) -> Result[Constraint, str]:
    weight_result: Result[Weight, str] = Weight.from_string(data["weight"])
    if not is_successful(weight_result):
        return Failure(weight_result.failure())

    match data["type"]:
        case ConstraintType.STAFF_UNAVAILABLE.value:
            return UnavailableStaffTime.create(
                name=data["name"],
                unavailability=data["unavailability"],
                weight=data["weight"],
            )
        case ConstraintType.CLASSROOM_UNAVAILABLE.value:
            return UnavailableClassroomTime.create(
                classroom_id=data["id"],
                unavailability=data["unavailability"],
                weight=data["weight"],
            )
        case ConstraintType.PREFERRED_EVENT.value:
            return Success(PreferredEvent(
                classroom=data["classroom"],
                instructor=data["instructor"],
                course=data["course"],
                group=data["group"],
                event_type=data["event_type"],
                preferred_time=data["preferred_time"],
                weight=data["weight"],
            ))
        case _:
            return Failure(f"Unknown constraint type: {data['type']}")
