# Staff Members

**Input Information**
- **ID**: Randomly generated (maybe a rule of identification ?)
- **Name**: [String]
- **Grad**: Enum (`Asistent`, `Lecturer`, `Conf`, `Prof`)

**Computational**
- **Priority**: `Asistent` < `Lecturer` < `Conf` < `Prof` (TBD)

# Classroom

**Input Information**
- **ID**: Format (C201)
- **Type**: Enum (`Lecture`, `Laboratory`)

# Events

**Input Information**
- **ID**: Format `[Semester][Initials of Name]` (generated)
- **Name**: [String]
- **Semester**: Range `[1-6]`
- **Optional Package**: Range `[1-3]`
- **Primary Instructors**: Array of IDs of instructors who will hold the lectures
- **Secondary Instructors**: Array of IDs of instructors who will hold the laboratories

**Notes**
- Optionals will have exactly **1 Lecture** (for all groups) and **3 Labs** (for all groups from either A, B, or E).
- Optionals may occur in the same time interval only if they are from different packages.
- Laboratories may be held by the Primary Instructors as well.
- If there are multiple Primary Instructors, they will be assigned the same time interval for the given course. They are considered to hold that course together.

**Computational**
- These events should be split by `Semester % 2` to create two divisions, resulting in timetables that are independent of each other.
- By knowing how many groups exist in each year (where a year means two semesters) and how they are distributed, we can compute all events (populate groups). **Take into consideration optional differences!**
- **Group**: Format `[1|2|3][A|B|E]`
- Primary and Secondary Instructors should not appear in the class because it's duplicated data.
- After the split, the only data needed for computation is **ID** and **Optional Package**.

**Additional Details Needed for Computational**: 
- Consider keeping a list of Primary and Secondary Instructors for reference.
