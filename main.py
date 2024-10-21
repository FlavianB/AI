class Classroom:
    def __init__(self, id, availability):
        self.id = id
        self.type = type # Lecture classroom or Lab classroom
        self.availability = availability # Dictionary of availability intervals, the key is the day and the value is a list of intervals

class Event:
    def __init__(self, id, type, group, duration, professor, assigned_time):
        self.id = id
        self.type = type # Lecture or Lab
        self.group = group # Group number
        self.duration = duration # Duration in hours, assumed 2
        self.professor = professor # Professor in charge of the course
        self.assigned_time = assigned_time # Assigned time, assumed None

class StaffMember:
    def __init__(self, name, type, availability, break_time, events):
        self.name = name
        self.type = type # Professor or Assistant
        self.availability = availability # Dictionary of availability intervals, the key is the day and the value is a list of intervals
        self.break_time = break_time # Break time in hours, assumed 0
        self.events = events # List of events assigned to the staff member