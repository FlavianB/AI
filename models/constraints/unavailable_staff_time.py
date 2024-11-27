from typing import Dict, List
from models.constraints.constants import ConstraintType, Weight
from models.constraints.constraint import Constraint
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful

from models.time_interval import TimeInterval

class UnavailableStaffTime(Constraint):
    __slots__ = '__name', '__unavailability'
    __name: str
    __unavailability: list[TimeInterval]

    def __init__(self, name: str, unavailability: list[TimeInterval], weight: Weight):
        super().__init__(ConstraintType.STAFF_UNAVAILABLE, weight)
        self.__name = name
        self.__unavailability = unavailability

    @staticmethod
    def create(name: str, unavailability: Dict[str, List[str]], weight: Weight) -> Result["UnavailableStaffTime", str]:
        err = ""
        time_intervals: list[TimeInterval] = []

        if not name.strip():
            err += 'Name of the staff member cannot be empty.\n'
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

        return Success(UnavailableStaffTime(name, time_intervals, weight))
    
    def get_name(self) -> str:
        return self.__name
    
    def get_time_intervals(self) -> list[TimeInterval]:
        return self.__unavailability
