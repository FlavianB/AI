import json
from typing import Optional

from returns.pipeline import is_successful
from models.classroom import Classroom
from models.staff_member import StaffMember
from models.event import Event

def _read_classrooms(data_set_path: str) -> Optional[list[Classroom]]:
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

def _read_staff_members(data_set_path: str) -> Optional[list[StaffMember]]:
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

def _read_events(data_set_path: str) -> Optional[list[Event]]:
    f = open(f'inputs/{data_set_path}/events.json')
    events_data = json.load(f)
    for event in events_data['events']:
        if 'optional_package' not in event:
            event['optional_package'] = None

    events = [Event.create(**event) for event in events_data['events']]
    return None if not events else [e.unwrap() for e in events]

def read_all_data(data_set_path: str) -> Optional[tuple[list[Classroom], list[StaffMember], list[Event]]]:
    classrooms = _read_classrooms(data_set_path)
    staff_members = _read_staff_members(data_set_path)
    events = _read_events(data_set_path)
    
    if staff_members is None or events is None:
        return None
    
    is_valid = True
    staff_members_ids = set(list(map(lambda x: x.get_id() ,staff_members)))

    for event in events:
        unknown_ids = set(event.get_primary_instructors()).union(set(event.get_secondary_instructors())) - staff_members_ids
        if unknown_ids:
            print(f"Ids for event {event.get_name()} are not corelated with any staff members with id {unknown_ids}.")
            is_valid = False
        
    return None if not classrooms or not staff_members or not events or not is_valid else (classrooms, staff_members, events)