from enum import Enum
from typing import Optional
from models.event import Event

class CourseType(Enum):
    LECTURE = 'Lecture'
    LABORATORY = 'Laboratory'

class Course:
    __event_id: str
    __type: CourseType
    __group: str
    __optional_package: Optional[int]
    __instructors: list[str]

    def __init__(self, event: Event, course_type: CourseType, group: str):
        self.__event_id = event.get_id()
        self.__type = course_type
        self.__group = group
        self.__optional_package = event.get_optional_package()

        self.__instructors = (event.get_primary_instructors() if course_type == CourseType.LECTURE 
                              else event.get_secondary_instructors())

    def get_event_id(self) -> str:
        return self.__event_id

    def get_type(self) -> CourseType:
        return self.__type

    def get_group(self) -> str:
        return self.__group

    def get_optional_package(self) -> Optional[int]:
        return self.__optional_package

    def get_instructors(self) -> list[str]:
        return self.__instructors

    def __str__(self):
        return (
            f"Course ID: {self.__event_id}\n"
            f"Type: {self.__type.value}\n"
            f"Group: {self.__group}\n"
            f"Optional Package: {self.__optional_package}\n"
            f"Instructors: {self.__instructors}\n"
        )
