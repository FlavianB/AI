from typing import Dict, List
from models.constraints.constraint import Constraint


class UnavailableStaffTime(Constraint):
    def __init__(self, name: str, unavailability: Dict[str, List[str]], weight: str):
        super().__init__("unavailable_staff_time", weight)
        self.name = name
        self.unavailability = unavailability
