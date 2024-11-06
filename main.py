from algorithms.bkt import BKTAlgorithm
from io_utils.reading_bkt import read_all_data
from io_utils.generating_data import generate_courses
from io_utils.reading_bkt import read_all_data

import argparse
import argcomplete

# PYTHON_ARGCOMPLETE_OK
parser = argparse.ArgumentParser(description="A CLI script with autocompletion.")

# Define some arguments
parser.add_argument("algorithm", choices=["bkt", "arc", "arc-accu"], help="Algorithm to use.")
parser.add_argument("--input", choices=["example_bkt", "example_create_error", "example_validate_error"], help="Input file to consider")

# Enable autocompletion with argcomplete
argcomplete.autocomplete(parser)

args = parser.parse_args()

data = read_all_data(args.input)
if data is None:
    exit(-1)
    
classrooms, staff_members, events = data
# print(classrooms[0])
# print(staff_members[0])
# print (classrooms[0])
# print("-----------------------------------------------------------")
# print(staff_members[0])
# print("-----------------------------------------------------------")
# print(events[0])
courses = generate_courses(events)
# for c in courses:
#     print(c)

algo = BKTAlgorithm(courses, classrooms, staff_members, events)
if not algo.backtrack(0):
    print("No schedule possible")
else:
    for solution in algo.solution:
        (course, (classroom, ids, interval)) = solution
        event = next(x for x in events if course.get_event_id() == x.get_id())
        profs = list(filter(lambda x: any(x.get_id() == s_id for s_id in ids), staff_members))
        print(event.get_name(), event.get_semester(), course.get_type(), course.get_group())
        print (classroom.get_id(), interval)
        for prof in profs:
            print (prof.get_name())
exit(0)

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
