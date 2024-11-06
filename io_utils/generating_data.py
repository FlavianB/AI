from models.event import Event
from models.course import Course, CourseType

from typing import List

def generate_courses(events: List[Event], semester: int) -> List[Course]:
    courses = []

    for event in events:
        # We will not add the events for the other semester
        if event.get_semester() != semester % 2:
            continue
        if 'Engleza' in event.get_name():
            for i in range (1, 6):
                courses.append(Course(event, CourseType.LABORATORY, f"A{i}"))
            for i in range (1, 5):
                courses.append(Course(event, CourseType.LABORATORY, f"B{i}"))
            for i in range (1, 4):
                courses.append(Course(event, CourseType.LABORATORY, f"E{i}"))  
            continue  
        if event.get_optional_package() is None:
            courses.append(Course(event, CourseType.LECTURE, "A"))
            courses.append(Course(event, CourseType.LECTURE, "B"))
            courses.append(Course(event, CourseType.LECTURE, "E"))
            for i in range (1, 6):
                courses.append(Course(event, CourseType.LABORATORY, f"A{i}"))
            for i in range (1, 5):
                courses.append(Course(event, CourseType.LABORATORY, f"B{i}"))
            for i in range (1, 4):
                courses.append(Course(event, CourseType.LABORATORY, f"E{i}"))
        else:
            courses.append(Course(event, CourseType.LECTURE, "ABE")) # There is a single lecture for optional courses
            courses.append(Course(event, CourseType.LABORATORY, "A"))
            courses.append(Course(event, CourseType.LABORATORY, "B"))
            courses.append(Course(event, CourseType.LABORATORY, "E"))
                
    return courses
