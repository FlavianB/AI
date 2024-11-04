

from enum import Enum
from typing import Optional
# from models.classroom import Classroom
# from models.staff_member import StaffMember

# The generated events
class CourseType(Enum):
    LECTURE = 'Lecture'
    Laboratory = 'Laboratory'

class Course:
    event_id: str
    type: CourseType
    group: str
    optional_package: Optional[int]
    instructors: list[int] 
    # Taking type in consideration instructors are either primary or secondary 