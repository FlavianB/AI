
from typing import Dict, List
from models.constraints.constraint import Constraint
from models.constraints.constants import ConstraintType, Weight
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful

from models.time_interval import TimeInterval

class UnavailableClassroomTime(Constraint):
    __slots__ = '__classroom_id', '__unavailability'
    __classroom_id: str
    __unavailability: list[TimeInterval]

    def __init__(self, classroom_id: str, unavailability: list[TimeInterval], weight: Weight):
        super().__init__(ConstraintType.CLASSROOM_UNAVAILABLE, weight)
        self.__classroom_id = classroom_id
        self.__unavailability = unavailability

    @staticmethod
    def create(classroom_id: str, unavailability: Dict[str, List[str]], weight: Weight) -> Result["UnavailableClassroomTime", str]:
        err = ""
        time_intervals: list[TimeInterval] = []

        if not classroom_id.strip():
            err += 'Id of the classroom cannot be empty.\n'
        if unavailability is None or not len(unavailability.keys()):
            err += "The constraint should contain at least one unavailablity interval.\n"

        for key, values in unavailability.items():
            for value in values:
                time_interval_result = TimeInterval.from_input(key, value)
                if not is_successful(time_interval_result):
                    err += time_interval_result.failure()
                else:
                    time_intervals.append(time_interval_result.unwrap())

        if err:
            return Failure(err)

        return Success(UnavailableClassroomTime(classroom_id, time_intervals, weight))
    
    def get_classroom_id(self) -> str:
        return self.__classroom_id
    
    def get_time_intervals(self) -> list[TimeInterval]:
        return self.__unavailability