from models.classroom import Classroom, ClassroomType
from models.constraints.constants import Weight
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
    solution: list[tuple[Course, AssignmentType]]  # List of (Course, Assignment)

    def __init__(self, courses: list[Course], classrooms: list[Classroom], staff_members: list[StaffMember], events: list[Event], constraints: list[Constraint]):
        self.lecture_classes = list(filter(lambda x: x.get_type() == ClassroomType.LECTURE, classrooms))
        self.laboratory_classes = list(filter(lambda x: x.get_type() == ClassroomType.LABORATORY, classrooms))
        self.events = events
        self.courses = courses
        self.staff_members = staff_members
        self.constraints = constraints
        self.solution = []

    def initialize_domains(self) -> dict[Course, list[AssignmentType]]:
        domains = {}

        # To be added preffered events
        # preffered_event_constraints = [constraint for constraint in self.constraints if isinstance(constraint, PreferredEvent)]

        # for constraint in self.constraints:
        #     if isinstance(constraint, PreferredEvent):
        #         course = next(course for course in self.courses if course.get_event_id() == constraint.get_course_name() and course.get_group() == constraint.get_group())
        #         domains[course] = []



        for course in self.courses:
            if domains.get(course) is not None:
                continue
            possible_assignments = []
            classrooms = self.lecture_classes if course.get_type() == CourseType.LECTURE else self.laboratory_classes
            for classroom in classrooms:
                for time_interval in TimeInterval:
                    if course.get_type() == CourseType.LECTURE:
                        staff_combinations = [course.get_instructors()]
                    else:
                        staff_combinations = [[staff_id] for staff_id in course.get_instructors()]
                    for staff_member_ids in staff_combinations:
                        assignment: AssignmentType = (classroom, staff_member_ids, time_interval)
                        if self.local_constraints_satisfied(course, assignment):
                            possible_assignments.append(assignment)
            domains[course] = possible_assignments
        return domains

    def local_constraints_satisfied(self, course, assignment: AssignmentType) -> bool:
        classroom, staff_member_ids, time_interval = assignment
        line, col = time_interval.convertToMatrixIndices()

        if course.get_type() == CourseType.LECTURE and classroom.get_type() != ClassroomType.LECTURE:
            return False
        if course.get_type() == CourseType.LABORATORY and classroom.get_type() != ClassroomType.LABORATORY:
            return False

        if classroom.availability[line, col] != 0:
            return False
        for staff_member_id in staff_member_ids:
            staff_member = next(member for member in self.staff_members if member.get_id() == staff_member_id)
            if staff_member.availability[line, col] != 0:
                return False
        # Additional local constraints can be added here
        return True

    def apply_global_hard_constraints(self):
        for constraint in self.constraints:
            if constraint.get_weight() != Weight.HARD:
                continue
            if isinstance(constraint, UnavailableClassroomTime):
                classroom = next(classroom for classroom in self.lecture_classes if classroom.get_id() == constraint.get_classroom_id())
                for interval in constraint.get_time_intervals():
                    line, col = interval.convertToMatrixIndices()
                    classroom.availability[line, col] = -1
                
            if isinstance(constraint, UnavailableStaffTime):
                staff_member = next(member for member in self.staff_members if member.get_name() == constraint.get_name())
                for interval in constraint.get_time_intervals():
                    line, col = interval.convertToMatrixIndices()
                    staff_member.availability[line, col] = -1

    def ac3(self, domains: dict[Course, list[AssignmentType]], assignment: dict[Course, AssignmentType] = {}) -> bool:
        """
        Applies the AC-3 algorithm to reduce the domains of the courses
        by enforcing arc consistency based on binary constraints.

        Args:
            domains (dict): A dictionary where keys are courses, and values are lists of possible assignments.
            assignment (dict): Current assignment of courses.

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

            if self.revise(domains, course_i, course_j, assignment):
                # If a domain is emptied, no solution is possible
                if not domains[course_i]:
                    return False
                # Add all neighbors of course_i back into the queue
                for course_k in self.courses:
                    if course_k != course_i and course_k != course_j:
                        queue.append((course_k, course_i))
        return True

    def revise(self, domains: dict[Course, list[AssignmentType]], course_i: Course, course_j: Course, assignment: dict[Course, AssignmentType]) -> bool:
        """
        Removes inconsistent values from the domain of course_i.

        Args:
            domains (dict): Current domains of the courses.
            course_i (Course): The course whose domain is being revised.
            course_j (Course): The course that imposes constraints on course_i.
            assignment (dict): Current assignment of courses.

        Returns:
            bool: True if the domain of course_i was revised, False otherwise.
        """
        revised = False
        assigned_j = course_j in assignment

        for assignment_i in domains[course_i][:]:
            if assigned_j:
                # course_j is assigned
                assignment_j = assignment[course_j]
                if not self.are_compatible(assignment_i, assignment_j, course_i, course_j):
                    domains[course_i].remove(assignment_i)
                    revised = True
            else:
                # course_j is not assigned
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
            # Check for group conflicts
            if not self.are_groups_compatible(course_i, course_j):
                return False
        return True

    def are_groups_compatible(self, course1: Course, course2: Course) -> bool:
        if course1.get_group() == "ABE" or course2.get_group() == "ABE":
            return True
        if len(course1.get_group()) == 2 and len(course2.get_group()) == 2:
            return course1.get_group() != course2.get_group()
        else:
            return course1.get_group() != course2.get_group()[0]

    def select_unassigned_variable(self, assignment: dict[Course, AssignmentType], domains: dict[Course, list[AssignmentType]]) -> Course:
        unassigned_courses = [c for c in self.courses if c not in assignment]
        # Use Minimum Remaining Values (MRV) heuristic
        min_domain_size = float('inf')
        selected_course = None
        for course in unassigned_courses:
            domain_size = len(domains[course])
            if domain_size < min_domain_size:
                min_domain_size = domain_size
                selected_course = course
        return selected_course

    def is_consistent(self, course: Course, value: AssignmentType, assignment: dict[Course, AssignmentType]) -> bool:
        for other_course, other_value in assignment.items():
            if not self.are_compatible(value, other_value, course, other_course):
                return False
        return True

    def backtrack(self, assignment: dict[Course, AssignmentType], domains: dict[Course, list[AssignmentType]]) -> bool:
        if len(assignment) == len(self.courses):
            self.solution = [(course, assignment[course]) for course in self.courses]
            return True

        course = self.select_unassigned_variable(assignment, domains)
        for value in domains[course]:
            if self.is_consistent(course, value, assignment):
                # Make a copy of assignment and domains
                local_assignment = assignment.copy()
                local_assignment[course] = value
                # Make a shallow copy of domains and deep copy the values
                local_domains = {c: domains[c][:] for c in domains}
                # Assign the value to the course and reduce its domain
                local_domains[course] = [value]

                # Apply AC-3 after the assignment
                if self.ac3(local_domains, local_assignment):
                    result = self.backtrack(local_assignment, local_domains)
                    if result:
                        return True
                # If AC-3 failed or recursive call failed, backtrack
        return False

    def solve(self) -> bool:
        """
        Executes the scheduling process using AC-3 and backtracking.
        """
        self.apply_global_hard_constraints()
        domains = self.initialize_domains()

        # Apply AC-3 as a preprocessing step and print the domains
        initial_ac3_result = self.ac3(domains)
        if not initial_ac3_result:
            print("No solution exists after applying AC-3 as preprocessing.")
            return False

        # Print the domains after AC-3 preprocessing
        print("\nDomains after AC-3 preprocessing:")
        for course in self.courses:
            print(f"Course {course.get_event_id()} domain:")
            for assignment in domains[course]:
                classroom, staff_member_ids, time_interval = assignment
                print(f"  Classroom: {classroom.get_id()}, Staff: {staff_member_ids}, Time: {time_interval}")

        assignment = {}

        if self.backtrack(assignment, domains):
            print("Solution found.")
            return True
        else:
            print("No solution exists.")
            return False
