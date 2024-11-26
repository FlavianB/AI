from enum import Enum

import numpy as np

class Day(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5

# We will consider the column a day of the week and the rows
# will be the intervals of that day
# If the value is 0 it is available. -1 means a hard constraint is in place.
# 1 means it was taken.
BASIC_AVAILABILITY: np.ndarray = np.zeros((6, 5), dtype=np.int8)
