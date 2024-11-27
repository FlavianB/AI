# PYTHON_ARGCOMPLETE_OK
from time import perf_counter
from icecream import ic

from algorithms.arc import ARCAlgorithm
from algorithms.bkt import BKTAlgorithm
from cli import cli
from io_utils.reading_bkt import read_all_data, _read_constraints
from io_utils.generating_data import generate_courses
from io_utils.output_file import OutputFile

ALGORITHM, INPUT, SEMESTER = cli.parse()
ic(ALGORITHM, INPUT, SEMESTER)

def main():
    data = read_all_data(INPUT)
    if data is None:
        exit(-1)
    
    classrooms, staff_members, events, constraints = data
    courses = generate_courses(events, SEMESTER)

    output_file = OutputFile('outputs/to_format.txt')
    time_start = perf_counter()
    if (ALGORITHM == 'bkt'):
        algo = BKTAlgorithm(courses, classrooms, staff_members, events)
        if not algo.backtrack(0):
            print("No schedule possible")
        else:
            for solution in algo.solution:
                (course, (classroom, ids, interval)) = solution
                event = next(x for x in events if course.get_event_id() == x.get_id())
                profs = list(filter(lambda x: any(x.get_id() == s_id for s_id in ids), staff_members))
                output_file.write_and_log(event.get_name(), event.get_semester(), course.get_type(), course.get_group())
                output_file.write_and_log(classroom.get_id(), interval)
                for prof in profs:
                    output_file.write_and_log(prof.get_name())
    elif (ALGORITHM == "counting-bkt"):
        algo = BKTAlgorithm(courses, classrooms, staff_members, events)

        print(algo.backtrack_counting(0))
    elif ALGORITHM == 'arc-bkt':
        algo = ARCAlgorithm(courses, classrooms, staff_members, events, constraints)
        if algo.solve():
            for solution in algo.solution:
                (course, (classroom, ids, interval)) = solution
                event = next(x for x in events if course.get_event_id() == x.get_id())
                profs = list(filter(lambda x: any(x.get_id() == s_id for s_id in ids), staff_members))
                output_file.write_and_log(event.get_name(), event.get_semester(), course.get_type(), course.get_group())
                output_file.write_and_log(classroom.get_id(), interval)
                for prof in profs:
                    output_file.write_and_log(prof.get_name())
        else:
            print("No schedule possible with ARC consistency.")
    else:
        print("Algorithm not implemented")

    time_finish = perf_counter()
    print (f"Time duration: {time_finish - time_start}")
    output_file.close()


if __name__ == '__main__':
    main()
