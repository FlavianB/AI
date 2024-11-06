from enum import Enum

from models.classroom import Classroom, ClassroomType
from models.course import Course, CourseType
from models.event import Event
from models.staff_member import StaffMember

'''
    We read M1 as interval: Monday 8:00-10:00
    Digit 1 means 8:00-10:00
    Digit 6 means 18:00-20:00
    M - Monday
    T - Tuesday
    ...
'''
class TimeInterval(Enum):
    M1 = 1,
    M2 = 2,
    M3 = 3,
    M4 = 4,
    M5 = 5,
    M6 = 6,

    T1 = 11,
    T2 = 12,
    T3 = 13,
    T4 = 14,
    T5 = 15,
    T6 = 16,

    W1 = 21,
    W2 = 22,
    W3 = 23,
    W4 = 24,
    W5 = 25,
    W6 = 26,

    TH1 = 31,
    TH2 = 32,
    TH3 = 33,
    TH4 = 34,
    TH5 = 35,
    TH6 = 36,

    F1 = 41,
    F2 = 42,
    F3 = 43,
    F4 = 44,
    F5 = 45,
    F6 = 46,

def are_groups_equal(group1: str, group2: str) -> bool:
    if group1 == 'ABE' or group2 == 'ABE':
        return True
    if len(group1) == 2 and len(group2) == 2:
        return group1 == group2
    else:
        return group1[0] == group2[0]

class BKTAlgorithm:
    staff_members: list[StaffMember]
    courses: list[Course]
    events: list[Event]
    lecture_classes: list[Classroom]
    laboratory_classes: list[Classroom]
    solution: list[tuple[Course, tuple[Classroom, list[str], TimeInterval]]] # str is list of staff_member_ids

    def __init__(self, courses: list[Course], classrooms: list[Classroom], staff_members: list[StaffMember], events: list[Event]):
        self.lecture_classes = list(filter(lambda x: x.get_type() == ClassroomType.LECTURE ,classrooms))
        self.laboratory_classes = list(filter(lambda x: x.get_type() == ClassroomType.LABORATORY ,classrooms))
        self.events = events
        self.courses = courses
        self.staff_members = staff_members
        self.solution = []

    def is_valid_assignment(self, course: Course, classroom: Classroom, staff_member_ids: list[str], time_interval: TimeInterval):
        event = next(event for event in self.events if event.get_id() == course.get_event_id())

        for solution in self.solution:
            course_, (classroom_, staf_id, time_interval_) = solution
            event_ = next(event for event in self.events if event.get_id() == course_.get_event_id())

            if time_interval_ == time_interval:
                # Check intersection of classroom with members
                if classroom_ == classroom or len(set(staff_member_ids) & set(staf_id)):
                    return False
                if (event.get_semester() == event_.get_semester()
                           and are_groups_equal(course_.get_group(), course.get_group())):
                    if course.get_optional_package() is None or course_.get_optional_package is None:
                        return False
                    if (course.get_optional_package() == course_.get_optional_package()):
                        return False
       
        return True
    def backtrack(self, course_index=0):
        if course_index == len(self.courses):
            return True
        
        course = self.courses[course_index]

        classrooms = self.lecture_classes if course.get_type() == CourseType.LECTURE else self.laboratory_classes
        for classroom in classrooms:
            for time_interval in TimeInterval:
                if (course.get_type() == CourseType.LECTURE):
                    if self.is_valid_assignment(course, classroom, course.get_instructors(), time_interval):
                        self.solution.append((course, (classroom, course.get_instructors(), time_interval))) # create solution
                        if self.backtrack(course_index + 1):
                            return True
                    
                        self.solution.pop()
                else:
                    for staff_member_id in course.get_instructors():
                        if self.is_valid_assignment(course, classroom, [staff_member_id], time_interval):
                            self.solution.append((course, (classroom, [staff_member_id], time_interval))) # create solution
                        
                            if self.backtrack(course_index + 1):
                                return True
                    
                            self.solution.pop()
        return False