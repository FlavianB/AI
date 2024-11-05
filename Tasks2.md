# Task Breakdown

### 1. Main Function: Call `read_all_data` and Validate Output
- In `main`, call the `read_all_data` function and ensure it works as expected.
- Verify that `read_all_data` returns data correctly, and handle cases where it returns `None`.

### 2. Example Input for Validation Testing
- Create an example input file in the `*inputs*` directory containing data that should trigger validation errors. 
- This file will help ensure our validation functions are working correctly by producing specific errors.
- Each folder of tests should contain an output_expected.md in which we write all the errors we should encounter based on the input so we can check with the actually output of our program

### 3. Rename Functions in `reading_bkt.py`
- Rename all functions in `reading_bkt.py` to begin with an underscore (`_`) to indicate internal use, except for the main function `read_all_data`.
- This renaming will enforce that only `read_all_data` is accessible outside the module.

### 4. Add Validation for `StaffMember` Properties
- Implement validation checks for `StaffMember` properties, ensuring:
  - **ID** is unique and correctly formatted.
  - **Name** is a non-empty string.
  - **Grad** is one of the predefined values (`Asistent`, `Lecturer`, `Conf`, `Prof`).

### 5. Validate Instructor IDs in Events
- Verify that all `primary_instructors` and `secondary_instructors` IDs in events exist in the list of valid `StaffMember` IDs.
- If any instructor ID does not match a valid `StaffMember` ID, print an error message indicating the mismatch.

### 6. Generate courses
- Implement `Course` class to respect encapsulation
- Generate based on events all the courses needed
- For now we will consider the groups static
    - List of groups: A1-A5,B1-B4,E1-E3
    - For the courses the group will be considered A,B,E
---

# Notes

- Ensure that error messages are descriptive, specifying the issue and the associated data.
- Run tests using the example input to confirm that each validation check works as expected.

# Further Considerations

- **Time Interval**: How should we consider time intervals in our domain?
- **Output Destination**: Should all data be logged to `output.log` in `inputs/example.bkt` or printed to the console?
- **Solution Type in `bkt.py`**: Is the current solution type optimal? Any suggestions for improvement?
