from tabulate import tabulate
from collections import defaultdict

time_map = {
    "M1": "Monday 08:00-10:00", "M2": "Monday 10:00-12:00", "M3": "Monday 12:00-14:00", "M4": "Monday 14:00-16:00", 
    "M5": "Monday 16:00-18:00", "M6": "Monday 18:00-20:00", "T1": "Tuesday 08:00-10:00", "T2": "Tuesday 10:00-12:00",
    "T3": "Tuesday 12:00-14:00", "T4": "Tuesday 14:00-16:00", "T5": "Tuesday 16:00-18:00", "T6": "Tuesday 18:00-20:00",
    "W1": "Wednesday 08:00-10:00", "W2": "Wednesday 10:00-12:00", "W3": "Wednesday 12:00-14:00", "W4": "Wednesday 14:00-16:00", "W5" : "Wednesday 16:00-18:00",  "W6" : "Wednesday 18:00-20:00",
    "TH1": "Thursday 08:00-10:00", "TH2": "Thursday 10:00-12:00", "TH3": "Thursday 12:00-14:00", "TH4": "Thursday 14:00-16:00", "TH5": "Thursday 16:00-18:00",
    "TH6": "Thursday 18:00-20:00","F1": "Friday 08:00-10:00", "F2": "Friday 10:00-12:00", "F3": "Friday 12:00-14:00", "F4": "Friday 14:00-16:00", "F5": "Friday 16:00-18:00"
}

def parse_file(file_path):
    data = []
    
    with open(file_path, 'r', encoding="utf-16") as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            course_info = lines[i].strip().split()
            course = course_info[0]  
            year = course_info[1]    
            course_type = course_info[2].replace("CourseType.", "")  
            group = course_info[3]  
            
            room_time = lines[i + 1].strip().split()
            room = room_time[0]  
            time = room_time[1].replace("TimeInterval.", "") 
            
            instructor = lines[i + 2].strip()  
            
            data.append({
                "Course": course,
                "Year": year,
                "Type": course_type,
                "Group": group,
                "Room": room,
                "Time": time,  
                "Instructor": instructor
            })
            
            i += 3
    return data

def group_by_group(data):
    grouped_data = defaultdict(list)
    for entry in data:
        grouped_data[entry['Group']].append(entry)
    return grouped_data

def format_timetable(grouped_data):
    timetable = {}
    
    for key, events in grouped_data.items():
        sorted_events = sorted(events, key=lambda x: list(time_map.keys()).index(x['Time']))  
        for event in sorted_events:
            event['Time'] = time_map.get(event['Time'], event['Time']) 
        
        timetable[key] = sorted_events
    
    return timetable

def display_timetable(timetable):
    for group, events in timetable.items():
        print(f"\n{group} Timetable")
        print(tabulate(events, headers="keys", tablefmt="grid"))
        print("\n" + "="*40)

file_path = 'to_format.txt' 
data = parse_file(file_path)
grouped_data = group_by_group(data)  
sorted_timetable = format_timetable(grouped_data)
display_timetable(sorted_timetable)
