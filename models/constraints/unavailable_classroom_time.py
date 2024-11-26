
from typing import Dict, List
from models.constraints.constraint import Constraint


class UnavailableClassroomTime(Constraint):
    def __init__(self, classroom_id: str, unavailability: Dict[str, List[str]], weight: str):
        super().__init__("unavailable_classroom_time", weight)
        self.classroom_id = classroom_id
        self.unavailability = unavailability
