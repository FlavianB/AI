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
from collections import deque

AssignmentType = tuple[Classroom, list[str], TimeInterval]

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
                for classroom in self.laboratory_classes:
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

    def ac3(self, domains: dict[Course, list[AssignmentType]]) -> bool:
        """
        Applies the AC-3 algorithm to reduce the domains of the courses
        by enforcing arc consistency based on binary constraints.

        Args:
            domains (dict): A dictionary where keys are courses, and values are lists of possible assignments.

        Returns:
            bool: True if the domains remain consistent, False if a domain is emptied.
        """
        queue = deque()
        
        # Initialize the queue with all arcs
        for course_i in self.courses:
            for course_j in self.courses:
                if course_i != course_j:
                    queue.append((course_i, course_j))

        while queue:
            course_i, course_j = queue.popleft()
            
            if self.revise(domains, course_i, course_j):
                # If a domain is emptied, no solution is possible
                if not domains[course_i]:
                    return False
                # Add all neighbors of course_i back into the queue
                for course_k in self.courses:
                    if course_k != course_i and course_k != course_j:
                        queue.append((course_k, course_i))
        
        return True

    def revise(self, domains: dict[Course, list[AssignmentType]], course_i: Course, course_j: Course) -> bool:
        """
        Removes inconsistent values from the domain of course_i.

        Args:
            domains (dict): Current domains of the courses.
            course_i (Course): The course whose domain is being revised.
            course_j (Course): The course that imposes constraints on course_i.

        Returns:
            bool: True if the domain of course_i was revised, False otherwise.
        """
        revised = False

        for assignment_i in domains[course_i][:]:
            # Check if there exists an assignment for course_j that is compatible
            if not any(self.are_compatible(assignment_i, assignment_j, course_i, course_j)
                       for assignment_j in domains[course_j]):
                domains[course_i].remove(assignment_i)
                revised = True
        
        return revised

    def are_compatible(self, assignment_i: AssignmentType, assignment_j: AssignmentType, course_i: Course, course_j: Course) -> bool:
        """
        Checks whether two assignments are compatible based on constraints.

        Args:
            assignment_i (AssignmentType): Assignment for course_i.
            assignment_j (AssignmentType): Assignment for course_j.
            course_i (Course): The first course.
            course_j (Course): The second course.

        Returns:
            bool: True if the assignments are compatible, False otherwise.
        """
        class_i, staff_i, time_i = assignment_i
        class_j, staff_j, time_j = assignment_j

        # Time conflict
        if time_i == time_j:
            # Check for classroom conflict
            if class_i == class_j:
                return False
            # Check for staff conflict
            if set(staff_i) & set(staff_j):
                return False
            if self.are_groups_compatible(course_i, course_j):
                return False
        # Additional constraints can be implemented here if needed
        return True

    def backtrack(self, course_index=0):
        if course_index == len(self.courses):
            return True

        course = self.courses[course_index]
        classrooms = self.lecture_classes if course.get_type() == CourseType.LECTURE else self.laboratory_classes
        for classroom in classrooms:
            for time_interval in TimeInterval:
                if course.get_type() == CourseType.LECTURE:
                    if self.is_valid_assignment(course, classroom, course.get_instructors(), time_interval):
                        self.solution.append((course, (classroom, course.get_instructors(), time_interval)))
                        if self.backtrack(course_index + 1):
                            return True
                        self.solution.pop()
                else:
                    for staff_member_id in course.get_instructors():
                        if self.is_valid_assignment(course, classroom, [staff_member_id], time_interval):
                            self.solution.append((course, (classroom, [staff_member_id], time_interval)))
                            if self.backtrack(course_index + 1):
                                return True
                            self.solution.pop()

        return False
    
    def is_valid_assignment(self, course: Course, classroom: Classroom, staff_member_ids: list[str], time_interval: TimeInterval):
        for solution_course, (solution_classroom, solution_staff, solution_time) in self.solution:
            if time_interval == solution_time:
                if solution_classroom == classroom or set(solution_staff) & set(staff_member_ids):
                    return False

                if not self.are_groups_compatible(course, solution_course):
                    return False

        return True

    def are_groups_compatible(self, course1: Course, course2: Course) -> bool:
        if course1.get_group() == "ABE" or course2.get_group() == "ABE":
            return True
        if len(course1.get_group()) == 2 and len(course2.get_group()) == 2:
            return course1.get_group() == course2.get_group()
        else:
            return course1.get_group() == course2.get_group()[0]

    def solve(self):
        """
        Executes the scheduling process using AC-3 and backtracking.
        """
        self.apply_global_hard_constraints()
        domains = self.initialize_domains()

        if not self.ac3(domains):
            print("No solution exists after applying AC-3.")
            return False
        exit(0)
        if self.backtrack():
            self.solution = [(course, domains[course][0]) for course in self.courses]  # First valid assignment
            return True
        else:
            return False
