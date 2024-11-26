from typing import Dict, List

from models.constraints.constraint import Constraint

class PreferredEvent(Constraint):
    def __init__(
        self,
        classroom: str,
        instructor: str,
        course: str,
        group: str,
        event_type: str,
        preferred_time: Dict[str, List[str]],
        weight: str,
    ):
        super().__init__("preferred_event", weight)
        self.classroom = classroom
        self.instructor = instructor
        self.course = course
        self.group = group
        self.event_type = event_type
        self.preferred_time = preferred_time

