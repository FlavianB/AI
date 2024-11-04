# Refactoring and Code Structure

### Centralized Read Function
- Move all read logic into a single function that:
  - Returns a list of events, staff members, and classrooms, or `None` (using `Optional`).
- In `main`, call only this function. 
  - If the return value is `None`, stop the program.
  - If valid data is returned, print all values for manual verification.

### Duplicate ID Checks
- Ensure there are no duplicate IDs in `staff_members` after reading. Perform this check within the staff member reading function, and print an error message from that function if duplicates are found.
- Similarly, check for duplicate IDs in `classrooms` within its respective reading function, and print an error if any duplicates are detected.

### Naming Conventions
- Use `id_` for IDs due to conflict with Python’s built-in `id()` function.
- Use `type_` similarly to avoid conflicts. For other parameters, suffixes are not required.

### Function Naming in `reading_bkt.py`
- Prefix reading functions in `reading_bkt.py` with an underscore (`_`) to indicate they are for internal use only.
- The main function that calls all other functions should **not** have an underscore, ensuring it’s the only function used outside the module.

### Installation and Dependencies
- If **Robert** does not have Python 3.12 installed, ensure it is installed before setting up with Poetry.

### Refactoring Tasks
- **Event Class**: Refactor the `Event` class (Assigned to **Paul**).

---

# Further Considerations

- **Time Interval**: How should we consider time intervals in our domain?
- **Output Destination**: Should all data be logged to `output.log` in `inputs/example.bkt` or printed to the console?
- **Solution Type in `bkt.py`**: Is the current solution type optimal? Any suggestions for improvement?
