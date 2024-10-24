import json


def get_constraint():
    constraint = {}

    # Get the type of constraint
    constraint_type = input("Type of constraint "
                            "(unavailable_staff_time, unavailable_classroom_time, preferred_event): ")

    # Add the type to the constraint
    constraint["type"] = constraint_type

    if constraint_type == "unavailable_staff_time":
        # Get details for unavailable_staff_time constraint
        constraint["name"] = input("Enter staff member's name: ")

        # Get unavailability for the staff member
        unavailability = {}
        more_days = True
        while more_days:
            day = input("Enter day of the week (e.g., Monday): ")
            times = input("Enter unavailable time intervals (comma separated, e.g., 08:00-10:00): ").split(",")
            unavailability[day] = [time.strip() for time in times]
            more_days = input("Add more days? (yes/no): ").lower() == "yes"

        constraint["unavailability"] = unavailability
        constraint["weight"] = input("Is this a hard or soft constraint? ")

    elif constraint_type == "unavailable_classroom_time":
        # Get details for unavailable_classroom_time constraint
        constraint["id"] = input("Enter classroom ID: ")

        # Get unavailability for the classroom
        unavailability = {}
        more_days = True
        while more_days:
            day = input("Enter day of the week (e.g., Monday): ")
            times = input("Enter unavailable time intervals (comma separated, e.g., 08:00-10:00): ").split(",")
            unavailability[day] = [time.strip() for time in times]
            more_days = input("Add more days? (yes/no): ").lower() == "yes"

        constraint["unavailability"] = unavailability
        constraint["weight"] = input("Is this a hard or soft constraint? ")

    elif constraint_type == "preferred_event":
        # Get details for preferred_event constraint
        constraint["instructor"] = input("Enter instructor's name: ")
        constraint["classroom"] = input("Enter classroom ID: ")
        constraint["group"] = input("Enter group name: ")
        constraint["course"] = input("Enter course name: ")
        constraint["event_type"] = input("Enter event type (Lecture or Lab): ")

        # Get preferred time for the event
        preferred_time = {}
        more_days = True
        while more_days:
            day = input("Enter day of the week (e.g., Monday): ")
            times = input("Enter preferred time intervals (comma separated, e.g., 10:00-12:00): ").split(",")
            preferred_time[day] = [time.strip() for time in times]
            more_days = input("Add more days? (yes/no): ").lower() == "yes"

        constraint["preferred_time"] = preferred_time
        constraint["weight"] = input("Is this a hard or soft constraint? ")

    else:
        print(f"Unknown constraint type: {constraint_type}")
        return None

    return constraint


def main():
    constraints = []
    more_constraints = True

    while more_constraints:
        constraint = get_constraint()
        if constraint:
            constraints.append(constraint)
        more_constraints = input("Add another constraint? (yes/no): ").lower() == "yes"

    # Write the constraints to a JSON file
    constraints_dict = {"constraints": constraints}

    # Write to prompted_constraints.json
    with open("prompted_constraints.json", "w") as file:
        json.dump(constraints_dict, file, indent=2)

    print("Constraints have been written to prompted_constraints.json")


if __name__ == "__main__":
    main()
