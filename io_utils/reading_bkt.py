import json
from typing import Optional

from returns.pipeline import is_successful
from returns.result import Success
from models.classroom import Classroom
from models.staff_member import StaffMember
from models.event import Event

def read_classrooms(data_set_path: str) -> Optional[list[Classroom]]:
    is_valid = True
    f = open(f'inputs/{data_set_path}/classrooms.json')
    classrooms_data = json.load(f)
    classrooms = [Classroom.create(**classroom) for classroom in classrooms_data['classrooms']]
    
    # Check for duplicate IDs
    seen_ids = set()
    for classroom in classrooms:
        if not is_successful(classroom):
            is_valid = False
            print(classroom.failure())
        else:
            classroom_id = classroom.unwrap().get_id()
            if classroom_id in seen_ids:
                is_valid = False
                print(f"Duplicate ID found in classrooms: {classroom_id}")
            else:
                seen_ids.add(classroom_id)

    return None if not is_valid else [classroom.unwrap() for classroom in classrooms]

def read_staff_members(data_set_path: str) -> Optional[list[StaffMember]]:
    is_valid = True
    f = open(f'inputs/{data_set_path}/staff_members.json')
    staff_members_data = json.load(f)
    staff_members = [StaffMember.create(**staff_member) for staff_member in staff_members_data['staff_members']]
    
    # Check for duplicate IDs
    seen_ids = set()
    for staff_member in staff_members:
        if not is_successful(staff_member):
            is_valid = False
            print(staff_member.failure())
        else:
            staff_member_id = staff_member.unwrap().get_id()
            if staff_member_id in seen_ids:
                is_valid = False
                print(f"Duplicate ID found in staff members: {staff_member_id}")
            else:
                seen_ids.add(staff_member_id)

    return None if not is_valid else [staff_member.unwrap() for staff_member in staff_members]

# Using results:
# def read_events(data_set_path: str) -> Optional[list[Event]]:
#     is_valid = True
#     f = open(f'inputs/{data_set_path}/events.json')
#     events_data = json.load(f)
#     events = [Event.create(**event) for event in events_data['events']]
#     for event in events:
#         if (not is_successful(event)):
#             is_valid = False
#             print(event.failure())
    
#     return None if not is_valid else [event.unwrap() for event in events]


# Without results:
def read_events(data_set_path: str) -> Optional[list[Event]]:
    f = open(f'inputs/{data_set_path}/events.json')
    events_data = json.load(f)
    events = [Event.create(**event) for event in events_data['events']]
    
    return None if not events else events

def read_all_data(data_set_path: str) -> Optional[list[list[Classroom], list[StaffMember], list[Event]]]:
    classrooms = read_classrooms(data_set_path)
    staff_members = read_staff_members(data_set_path)
    events = read_events(data_set_path)

    return None if not classrooms or not staff_members or not events else [classrooms, staff_members, events]