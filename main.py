import json
from models.classroom import Classroom
# Here we have the basic availability for the classrooms and instructors
x = Classroom.create(id_='C201', type_='Lecturea')
print (x)
exit()
basic_availability = {
    "Monday": ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"],
    "Tuesday": ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"],
    "Wednesday": ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"],
    "Thursday": ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"],
    "Friday": ["08:00-10:00", "10:00-12:00", "12:00-14:00", "14:00-16:00", "16:00-18:00", "18:00-20:00"]
}


# class Classroom:
#     availability = basic_availability

#     def __init__(self, id, type):
#         self.id = id
#         self.type = type

#     def __str__(self):
#         availability_str = "\n".join([f"{day}: {', '.join(intervals)}" for day, intervals in self.availability.items()])
#         return (
#             f"Classroom: {self.id}\n"
#             f"Type: {self.type}\n"
#             f"Availability:\n{availability_str}"
#         )


class Event:
    assigned_time = None
    classroom = None
    instructor = None

    def __init__(self, type, group, course):
        self.type = type
        self.group = group
        self.course = course

    def __str__(self):
        return (
            f"Event: {self.group}\n"
            f"Classroom: {self.classroom}\n"
            f"Course: {self.course}\n"
            f"Type: {self.type}\n"
            f"Instructor: {self.instructor}\n"
            f"Assigned Time: {self.assigned_time}"
        )


class StaffMember:
    availability = basic_availability

    def __init__(self, name, position, events=None):
        self.name = name
        self.position = position
        self.events = events

    def __str__(self):
        availability_str = "\n".join([f"{day}: {', '.join(intervals)}" for day, intervals in self.availability.items()])
        events_str = "\n".join([str(event) for event in self.events]) if self.events else "No events assigned"

        return (
            f"Staff Member: {self.name}\n"
            f"Position: {self.position}\n"
            f"Availability:\n{availability_str}\n"
            f"Assigned Events:\n{events_str}"
        )


# We will parse the data from the JSON files
f = open('classrooms.json')
classrooms_data = json.load(f)
classrooms = [Classroom(**classroom) for classroom in classrooms_data['classrooms']]

f = open('events.json')
events_data = json.load(f)
events = [Event(**event) for event in events_data['events']]

f = open('staff_members.json')
staff_members_data = json.load(f)
staff_members = [StaffMember(**staff_member) for staff_member in staff_members_data['staff']]
print(staff_members[0])


def process_soft_constraints(constraints_file):
    f = open(constraints_file)
    constraints_data = json.load(f)['constraints']

    # Extract the soft constraints
    return [constraint for constraint in constraints_data if constraint.get('weight') == 'soft']


def process_hard_constraints(constraints_file):
    # We will parse the constraints
    f = open(constraints_file)
    constraints_data = json.load(f)['constraints']
    # We will parse the staff constraints
    hard_unavailable_staff_time_constraints = filter(
        lambda constraint: constraint['type'] == 'unavailable_staff_time' and constraint['weight'] == 'hard',
        constraints_data)
    for constraint in hard_unavailable_staff_time_constraints:
        staff_member = next((staff_member for staff_member in staff_members if staff_member.name == constraint['name']),
                            None)
        for day, times in constraint['unavailability'].items():
            if day in staff_member.availability:
                # Remove each unavailable time from the available times
                for time in times:
                    if time in staff_member.availability[day]:
                        staff_member.availability[day].remove(time)

    print('--------------------------')
    print(staff_members[0])

    print('--------------------------')
    print(classrooms[0])
    # We will parse the classroom constraints
    hard_unavailable_classroom_time_constraints = filter(
        lambda constraint: constraint['type'] == 'unavailable_classroom_time' and constraint['weight'] == 'hard',
        constraints_data)
    for constraint in hard_unavailable_classroom_time_constraints:
        classroom = next((classroom for classroom in classrooms if classroom.id == constraint['id']), None)
        if classroom:
            for day, times in constraint['unavailability'].items():
                # Remove each unavailable time from the available times
                for time in times:
                    if time in classroom.availability[day]:
                        classroom.availability[day].remove(time)

    print('--------------------------')
    print(classrooms[0])

    print('--------------------------')
    print(events[0])
    # We will parse the event constraints
    hard_event_constraints = filter(
        lambda constraint: constraint['type'] == 'preferred_event' and constraint['weight'] == 'hard',
        constraints_data)
    for constraint in hard_event_constraints:
        event = next((event for event in events if event.group == constraint['group']
                      and event.course == constraint['course']
                      and event.type == constraint['event_type']), None)
        if event:
            if constraint['preferred_time']:
                event.assigned_time = constraint['preferred_time']
            if constraint['instructor']:
                event.instructor = constraint['instructor']
            if constraint['classroom']:
                event.classroom = constraint['classroom']

    print('--------------------------')
    print(events[0])


process_hard_constraints('constraints.json')

soft_constraints = process_soft_constraints('constraints.json')
