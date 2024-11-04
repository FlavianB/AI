import json
from typing import Optional

from returns.pipeline import is_successful
from returns.result import Success
from models.classroom import Classroom


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