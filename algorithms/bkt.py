
import time
from typing import Optional
from models.classroom import Classroom, ClassroomType
from models.constants import Day
from models.course import Course, CourseType
from models.staff_member import StaffMember


class BKTAlgorithm:
    staff_members: list[StaffMember]
    courses: list[Course] # Events ? Not really
    lecture_classes: list[Classroom]
    laboratory_classes: list[Classroom]
    solution: list[Optional[tuple[Course, tuple[Classroom, StaffMember]]]] # we need a domain model for TimeInterval ?

    def __init__(self, classrooms: list[Classroom]):
        self.lecture_classes = list(filter(lambda x: x.get_type() == ClassroomType.LECTURE ,classrooms))
        self.laboratory_classes = list(filter(lambda x: x.get_type() == ClassroomType.LABORATORY ,classrooms))

        self.laboratory_classes[0].availability[Day.MONDAY] = ["8000"]
        for c in self.laboratory_classes:
            print(c)
        for c in classrooms: 
            print (c)

    def is_valid_assignment(self, course, classroom, time_interval):
         return True
    
    def backtrack(self, course_index=0):
        if course_index == len(self.courses):
            return True
        
        course = self.courses[course_index]

        classrooms = self.lecture_classes if course.__type == CourseType.LECTURE else self.laboratory_classes

        for classroom in classrooms:
            # for time_interval in self.time_interval:
                time_interval = 0
                if self.is_valid_assignment(course, classroom, time_interval):
                    self.solution.append(None) # create solution
                    
                    if self.backtrack(course_index + 1):
                         return True
                    
                    self.solution.pop()
        return False
    
        # idee:
        # for classroom in classrooms:
        #      for prof in profs:
        #           for course in courses:
        #             time_intervals = intersectia dintre classroom.availability si prof.availability
        #             for time_interval in time_intervals:
        #                 if is_valid(time_interval, course, clasroom, prog):
        #                     etc


        # mergem prin toate cursurile recursiv
        # alegem un classroom un functie de type ul cursului pentru M1(monday 8:00-10:00)
        # daca gasim ne uitam la profii care pot sa predea in M1
        # daca gasim unul cream un solution si dam append
        # daca nu gasim un prof disponibil sau nu gasim un classroom disponibil mergem in M2
        # cum verificam sa nu aiba studentii in aceasi ora 2 materii/cursuri ? Trecem prin solutions ??
        # precalculam si TimeInterval pentru fiecare grupa ?? adica 12 * 3 grupe
        # nu precalculam nu optimizam inca asta trebuie pusa pe foaie
        # deci vom trece prin solution urile actuale si vedem daca se intercaleaza

        # ORdine
        # Alegem cursul
        # Alegem classroomul
        # Alegem prof
        # Verificam grupa