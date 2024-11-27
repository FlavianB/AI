from typing import Dict

from models.constraints.constants import ConstraintType, Weight
from models.constraints.constraint import Constraint
from models.course import CourseType
from models.time_interval import TimeInterval
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful

class PreferredEvent(Constraint):
    __slots__ = '__classroom', '__instructor', '__course', '__group', '__event_type', '__preferred_time'
    __classroom: str
    __preferred_time: list[TimeInterval]
    __instructor: str
    __course: str
    __group: str
    __event_type: CourseType

    def __init__(
        self,
        classroom: str,
        instructor: str,
        course: str,
        group: str,
        event_type: CourseType,
        preferred_time: list[TimeInterval],
        weight: Weight,
    ):
        super().__init__(ConstraintType.PREFERRED_EVENT, weight)
        self.__classroom = classroom
        self.__instructor = instructor
        self.__course = course
        self.__group = group
        self.__event_type = event_type
        self.__preferred_time = preferred_time

    @staticmethod
    def create(
        classroom: str,
        instructor: str,
        course: str,
        group: str,
        event_type: str,
        preferred_time: Dict[str, list[str]],
        weight: Weight,
        ) -> Result["PreferredEvent", str]:
        err = ""
        time_intervals: list[TimeInterval] = []

        # if not classroom_id.strip():
        #     err += 'Id of the classroom cannot be empty.\n'
        # if unavailability is None or not len(unavailability.keys()):
        #     err += "The constraint should contain at least one unavailablity interval.\n"

        # for key, values in unavailability.items():
        #     for value in values:
        #         time_interval_result = TimeInterval.from_input(key, value)
        #         if not is_successful(time_interval_result):
        #             err += time_interval_result.failure()
        #         else:
        #             time_intervals.append(time_interval_result.unwrap())

        # if err:
        #     return Failure(err)

        return Success(PreferredEvent(classroom, instructor ,course, group, CourseType.LECTURE, preferred_time=[TimeInterval.F1], weight=weight))
    
    def get_classroom_id(self) -> str:
        return self.__classroom
    
    def get_time_intervals(self) -> list[TimeInterval]:
        return self.__preferred_time
    def get_course_type(self) -> CourseType:
        return self.__event_type
    def get_instructor_name(self) -> str:
        return self.__instructor
    def get_course_name(self) -> str:
        return self.__course
    def get_group(self) -> str:
        return self.__group
