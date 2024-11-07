from models.classroom import Classroom, ClassroomType
from models.course import Course, CourseType
from models.event import Event
from models.staff_member import StaffMember
from models.time_interval import TimeInterval

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

            if time_interval_ != time_interval:
                continue
                # Check intersection of classroom with members
            if classroom_ == classroom or len(set(staff_member_ids) & set(staf_id)):
                return False
            
            if not (event.get_semester() == event_.get_semester()
                        and are_groups_equal(course_.get_group(), course.get_group())):
                continue
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
    
    def backtrack_counting(self, course_index=0):
        if course_index == len(self.courses):
            # for solution in self.solution:
            #     (course, (classroom, ids, interval)) = solution
            #     event = next(x for x in self.events if course.get_event_id() == x.get_id())
            #     profs = list(filter(lambda x: any(x.get_id() == s_id for s_id in ids), self.staff_members))
            #     print(event.get_name(), event.get_semester(), course.get_type(), course.get_group())
            #     print (classroom.get_id(), interval)
            #     for prof in profs:
            #         print (prof.get_name())
            # print("--------------------")
            return 1
        count = 0
        course = self.courses[course_index]

        classrooms = self.lecture_classes if course.get_type() == CourseType.LECTURE else self.laboratory_classes
        for classroom in classrooms:
            for time_interval in TimeInterval:
                if (course.get_type() == CourseType.LECTURE):
                    if self.is_valid_assignment(course, classroom, course.get_instructors(), time_interval):
                        self.solution.append((course, (classroom, course.get_instructors(), time_interval))) # create solution
                        count += self.backtrack_counting(course_index + 1)

                        self.solution.pop()
                else:
                    for staff_member_id in course.get_instructors():
                        if self.is_valid_assignment(course, classroom, [staff_member_id], time_interval):
                            self.solution.append((course, (classroom, [staff_member_id], time_interval))) # create solution
                        
                            count += self.backtrack_counting(course_index + 1)
                    
                            self.solution.pop()
        return count