# Tasks
Change time interval of classrooms, ... in a matrix 6X5. Columns will be the days, rows will be a time interval of that day.
Add constraints class (In progress)
Validate state of constraint classes (In progress)

Added directory models/constaints in which we will have all type of constraints.
Added in io_utils/reading_bkt.py the function _read_constraints which is then called in read_all_data.
Modified main.py to have the constraints avaialble in our program.
Added alogrithms/arc.py. Here the arc-consistency algorithm will live.

-------------

Apply constraints to all of them.
Probably one more value should be added to the Constraint class like value [1-5] because our soft constraints should not be added directly as a hard constraint.

Implement arc-consistency algorithm.
-   Implement just arc-consistency without the backtracking. Basically just make a choice and afterwards apply arc-consistency, check the domain to ensure to algorithm works as expected.
- After the first step is done then the integration in backtracking should be trivial.

# Improvements
- Output format(for manual testing)
- Testing bkt algorithm(complex solutions) Fail cases, Hard cases