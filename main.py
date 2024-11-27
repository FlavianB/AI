# PYTHON_ARGCOMPLETE_OK
from time import perf_counter
from icecream import ic

from algorithms.arc import ARCAlgorithm
from algorithms.bkt import BKTAlgorithm
from cli import cli
from io_utils.reading_bkt import read_all_data, _read_constraints
from io_utils.generating_data import generate_courses
from io_utils.output_file import OutputFile

ALGORITHM, INPUT, SEMESTER = cli.parse()
ic(ALGORITHM, INPUT, SEMESTER)

def main():
    data = read_all_data(INPUT)
    if data is None:
        exit(-1)
    
    classrooms, staff_members, events, constraints = data
    courses = generate_courses(events, SEMESTER)
    # for i in courses:
    #     print (i)

    output_file = OutputFile('outputs/to_format.txt')
    time_start = perf_counter()
    if (ALGORITHM == 'bkt'):
        algo = BKTAlgorithm(courses, classrooms, staff_members, events)
        if not algo.backtrack(0):
            print("No schedule possible")
        else:
            for solution in algo.solution:
                (course, (classroom, ids, interval)) = solution
                event = next(x for x in events if course.get_event_id() == x.get_id())
                profs = list(filter(lambda x: any(x.get_id() == s_id for s_id in ids), staff_members))
                output_file.write_and_log(event.get_name(), event.get_semester(), course.get_type(), course.get_group())
                output_file.write_and_log(classroom.get_id(), interval)
                for prof in profs:
                    output_file.write_and_log(prof.get_name())
    elif (ALGORITHM == "counting-bkt"):
        algo = BKTAlgorithm(courses, classrooms, staff_members, events)

        print(algo.backtrack_counting(0))
    elif ALGORITHM == 'arc':
        algo = ARCAlgorithm(courses, classrooms, staff_members, events, constraints)
        if algo.solve():
            for solution in algo.solution:
                (course, (classroom, ids, interval)) = solution
                event = next(x for x in events if course.get_event_id() == x.get_id())
                profs = list(filter(lambda x: any(x.get_id() == s_id for s_id in ids), staff_members))
                output_file.write_and_log(event.get_name(), event.get_semester(), course.get_type(), course.get_group())
                output_file.write_and_log(classroom.get_id(), interval)
                for prof in profs:
                    output_file.write_and_log(prof.get_name())
        else:
            print("No schedule possible with ARC consistency.")
    else:
        print("Algorithm not implemented")

    time_finish = perf_counter()
    print (f"Time duration: {time_finish - time_start}")
    output_file.close()


if __name__ == '__main__':
    main()
# def process_soft_constraints(constraints_file):
#     f = open(constraints_file)
#     constraints_data = json.load(f)['constraints']

#     # Extract the soft constraints
#     return [constraint for constraint in constraints_data if constraint.get('weight') == 'soft']


# def process_hard_constraints(constraints_file):
#     # We will parse the constraints
#     f = open(constraints_file)
#     constraints_data = json.load(f)['constraints']
#     # We will parse the staff constraints
#     hard_unavailable_staff_time_constraints = filter(
#         lambda constraint: constraint['type'] == 'unavailable_staff_time' and constraint['weight'] == 'hard',
#         constraints_data)
#     for constraint in hard_unavailable_staff_time_constraints:
#         staff_member = next((staff_member for staff_member in staff_members if staff_member.name == constraint['name']),
#                             None)
#         for day, times in constraint['unavailability'].items():
#             if day in staff_member.availability:
#                 # Remove each unavailable time from the available times
#                 for time in times:
#                     if time in staff_member.availability[day]:
#                         staff_member.availability[day].remove(time)

#     print('--------------------------')
#     print(staff_members[0])

#     print('--------------------------')
#     print(classrooms[0])
#     # We will parse the classroom constraints
#     hard_unavailable_classroom_time_constraints = filter(
#         lambda constraint: constraint['type'] == 'unavailable_classroom_time' and constraint['weight'] == 'hard',
#         constraints_data)
#     for constraint in hard_unavailable_classroom_time_constraints:
#         classroom = next((classroom for classroom in classrooms if classroom.id == constraint['id']), None)
#         if classroom:
#             for day, times in constraint['unavailability'].items():
#                 # Remove each unavailable time from the available times
#                 for time in times:
#                     if time in classroom.availability[day]:
#                         classroom.availability[day].remove(time)

#     print('--------------------------')
#     print(classrooms[0])

#     print('--------------------------')
#     print(events[0])
#     # We will parse the event constraints
#     hard_event_constraints = filter(
#         lambda constraint: constraint['type'] == 'preferred_event' and constraint['weight'] == 'hard',
#         constraints_data)
#     for constraint in hard_event_constraints:
#         event = next((event for event in events if event.group == constraint['group']
#                       and event.course == constraint['course']
#                       and event.type == constraint['event_type']), None)
#         if event:
#             if constraint['preferred_time']:
#                 event.assigned_time = constraint['preferred_time']
#             if constraint['instructor']:
#                 event.instructor = constraint['instructor']
#             if constraint['classroom']:
#                 event.classroom = constraint['classroom']

#     print('--------------------------')
#     print(events[0])


# process_hard_constraints('constraints.json')

# soft_constraints = process_soft_constraints('constraints.json')
