from models.classroom import Classroom, ClassroomType
from models.constraints.constraint import Constraint
from models.constraints.preffered_event import PreferredEvent
from models.constraints.unavailable_classroom_time import UnavailableClassroomTime
from models.constraints.unavailable_staff_time import UnavailableStaffTime
from models.course import Course, CourseType
from models.event import Event
from models.staff_member import StaffMember
from models.time_interval import TimeInterval
from icecream import ic

AssignmentType = tuple[Classroom, list[str], TimeInterval]

# The main function is solve
# in solve we first apply all hard constraints(yet to be implemented)
# we initilize all the possible domains without those which creates conflicts 
# with the hard constraints
# we trim down the domain by applying ac3
# afterwards we do the backtracking
class ARCAlgorithm:
    staff_members: list[StaffMember]
    courses: list[Course]
    events: list[Event]
    lecture_classes: list[Classroom]
    laboratory_classes: list[Classroom]
    constraints: list[Constraint]
    # solution: list[tuple[Course, tuple[Classroom, list[str], TimeInterval]]] # str is list of staff_member_ids

    def __init__(self, courses: list[Course], classrooms: list[Classroom], staff_members: list[StaffMember], events: list[Event], constraints: list[Constraint]):
        self.lecture_classes = list(filter(lambda x: x.get_type() == ClassroomType.LECTURE ,classrooms))
        self.laboratory_classes = list(filter(lambda x: x.get_type() == ClassroomType.LABORATORY ,classrooms))
        self.events = events
        self.courses = courses
        self.staff_members = staff_members
        self.constraints = constraints
        self.solution = []
    
    def initialize_domains(self):
        domains = {}
        for course in self.courses:
            possible_assignments = []
            classrooms = self.lecture_classes if course.get_type() == CourseType.LECTURE else self.laboratory_classes
            for classroom in classrooms:
                for time_interval in TimeInterval:
                    if course.get_type() == CourseType.LECTURE:
                        staff_combinations = [course.get_instructors()]
                    else:
                        staff_combinations = [[staff_id] for staff_id in course.get_instructors()]
                    for staff_member_ids in staff_combinations:
                        assignment: AssignmentType  = (classroom, staff_member_ids, time_interval)
                        if self.local_constraints_satisfied(course, assignment):
                            possible_assignments.append(assignment)
            domains[course] = possible_assignments
        return domains

    def local_constraints_satisfied(self, course, assignment: AssignmentType) -> bool:
        # Check constraints that involve only the course and the assignment
        classroom, staff_member_ids, time_interval = assignment
        # Check if the classroom type matches the course type
        line, col = time_interval.convertToMatrixIndices()

        if course.get_type() == CourseType.LECTURE and classroom.get_type() != ClassroomType.LECTURE:
            return False
        if course.get_type() == CourseType.LABORATORY and classroom.get_type() != ClassroomType.LABORATORY:
            return False
        
        if classroom.availability[line, col] != 0:
            return False
        for staff_member_id in staff_member_ids:
            staff_member = next(member for member in self.staff_members if member.get_id() == staff_member_id)
            if staff_member.availability[line,col] != 0:
                return False
        # Additional local constraints can be added here
        return True
    
    def apply_global_hard_constraints(self):
        for constraint in self.constraints:
            # we will hardcode the constraints for now
            if constraint.weight != 'hard':
                continue
            if isinstance(constraint, UnavailableClassroomTime):
                classroom = next(classroom for classroom in self.lecture_classes if classroom.get_id() == constraint.classroom_id)
                classroom.availability[:, :] = -1
                classroom.availability[:, 0] = 0
                # classroom.availability[0,3] = -1
                
            if isinstance(constraint, UnavailableStaffTime):
                staff_member = next(member for member in self.staff_members if member.get_name() == constraint.name)
                # staff_member.availability[0,2] = -1
                # staff_member.availability[0,3] = -1

                pass
            if isinstance(constraint, PreferredEvent):
                pass
        pass

    def ac3(self, domains):
        pass

    def backtrack(self, assignment, domains):
        pass

    def solve(self):
        self.apply_global_hard_constraints()
        domains: dict[Course, list[AssignmentType]] = self.initialize_domains()
        ac3_result = self.ac3(domains)
        if not ac3_result:
            print("No solution exists after applying AC-3.")
            return False
        assignment = {}
        result = self.backtrack(assignment, domains)
        if result:
            print("Solution found.")
            return True
        else:
            print("No solution exists.")
            return False
        # print(len(domains[self.courses[1]]))
        # su = 0
        # print(sum(len(value) for value in domains.values()))
            # print (i)
            # break
        # print (su)
