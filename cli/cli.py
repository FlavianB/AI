import argparse
import os

import argcomplete

class Args:
    algorithm: str
    input: str
    semester: int

def parse() -> tuple[str, str, int]:
    input_file: str = 'example_bkt'
    algorithm: str = 'bkt'
    semester: int = 1

    # For now autocomplete works only macos/Linux
    # if (os.name == 'posix'):
    parser = argparse.ArgumentParser(description="A CLI script with autocompletion.")

    # Define some arguments
    parser.add_argument("algorithm", choices=["bkt", "counting-bkt", "arc-preproc", "arc-bkt"], help="Algorithm to use.")
    parser.add_argument("semester", choices=["1", "2"], help="For which semester should we generate the timetable")
    parser.add_argument("input", choices=["example_bkt", "example_hard", "example_validate_error", "example_full", "example_cannot_generate", "example_not_enough_staff", "example_too_many_groups", "example_small_sample"], help="Input file to consider")

    # Enable autocompletion with argcomplete
    argcomplete.autocomplete(parser)

    args = parser.parse_args(namespace=Args)
    input_file = args.input
    semester = int(args.semester)
    algorithm = args.algorithm
    return (algorithm, input_file, semester)