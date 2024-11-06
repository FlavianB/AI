

from enum import Enum
from typing import Optional

from models.event import Event
# from models.classroom import Classroom
# from models.staff_member import StaffMember

# The generated events
class CourseType(Enum):
    LECTURE = 'Lecture'
    Laboratory = 'Laboratory'

class Course:
    __event_id: str
    __type: CourseType
    __group: str
    __optional_package: Optional[int]
    __instructors: list[int] 

    def __init__(self, event: Event):
        self.__event_id = event.get_id()
    # Taking type in consideration instructors are either primary or secondary 