import json
from typing import Optional

from returns.pipeline import is_successful
from returns.result import Success
from models.classroom import Classroom
from models.staff_member import StaffMember

def read_classrooms(data_set_path: str) -> Optional[list[Classroom]]:
    is_valid = True
    f = open(f'inputs/{data_set_path}/classrooms.json')
    classrooms_data = json.load(f)
    classrooms = [Classroom.create(**classroom) for classroom in classrooms_data['classrooms']]
    for classroom in classrooms:
        if(not is_successful(classroom)):
            is_valid = False
            print(classroom.failure())

    return None if not is_valid else [classroom.unwrap() for classroom in classrooms]

def read_staff_members(data_set_path: str) -> Optional[list[StaffMember]]:
    is_valid = True
    f = open(f'inputs/{data_set_path}/staff_members.json')
    staff_members_data = json.load(f)
    staff_members = [StaffMember.create(**staff_member) for staff_member in staff_members_data['staff_members']]
    for staff_member in staff_members:
        if(not is_successful(staff_member)):
            is_valid = False
            print(staff_member.failure())
    
    return None if not is_valid else [staff_member.unwrap() for staff_member in staff_members]
