from typing import Any, Dict
from models.constraints.constraint import Constraint
from models.constraints.preffered_event import PreferredEvent
from models.constraints.unavailable_classroom_time import UnavailableClassroomTime
from models.constraints.unavailable_staff_time import UnavailableStaffTime
from returns.result import Result, Failure

#  Result[Constraint, str]:
def create_constraint(data: Dict[str, Any]) -> Constraint:
    if data["type"] == "unavailable_staff_time":
        # return Failure("Not implemented")
        return UnavailableStaffTime(
            name=data["name"],
            unavailability=data["unavailability"],
            weight=data["weight"],
        )
    elif data["type"] == "unavailable_classroom_time":
        # return Failure("Not implemented")
        return UnavailableClassroomTime(
            classroom_id=data["id"],
            unavailability=data["unavailability"],
            weight=data["weight"],
        )
    elif data["type"] == "preferred_event":
        # return Failure("Not implemented")
        return PreferredEvent(
            classroom=data["classroom"],
            instructor=data["instructor"],
            course=data["course"],
            group=data["group"],
            event_type=data["event_type"],
            preferred_time=data["preferred_time"],
            weight=data["weight"],
        )
    else:
        # return Failure
        raise Exception(f"Unknown constraint type: {data['type']}")
