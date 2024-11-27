from enum import Enum
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful

class Day(Enum):
    MONDAY = ("Monday", 1)
    TUESDAY = ("Tuesday", 2)
    WEDNESDAY = ("Wednesday", 3)
    THURSDAY = ("Thursday", 4)
    FRIDAY = ("Friday", 5)

    @staticmethod
    def from_string(day: str) -> Result["Day", str]:
        for d in Day:
            if d.value[0].lower() == day.lower():
                return Success(d)
        return Failure(f"Invalid day '{day}'.\n")

class Interval(Enum):
    INTERVAL_1 = ("08:00-10:00", 1)
    INTERVAL_2 = ("10:00-12:00", 2)
    INTERVAL_3 = ("12:00-14:00", 3)
    INTERVAL_4 = ("14:00-16:00", 4)
    INTERVAL_5 = ("16:00-18:00", 5)
    INTERVAL_6 = ("18:00-20:00", 6)

    @staticmethod
    def from_string(interval: str) -> Result["Interval", str]:
        for d in Interval:
            if d.value[0].lower() == interval.lower():
                return Success(d)
        return Failure(f"Invalid time interval '{interval}'.\n")

'''
    We read M1 as interval: Monday 8:00-10:00
    Digit 1 means 8:00-10:00
    Digit 6 means 18:00-20:00
    M - Monday
    T - Tuesday
    ...
    F - Friday
'''
class TimeInterval(Enum):
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4
    M5 = 5
    M6 = 6

    T1 = 11
    T2 = 12
    T3 = 13
    T4 = 14
    T5 = 15
    T6 = 16

    W1 = 21
    W2 = 22
    W3 = 23
    W4 = 24
    W5 = 25
    W6 = 26

    TH1 = 31
    TH2 = 32
    TH3 = 33
    TH4 = 34
    TH5 = 35
    TH6 = 36

    F1 = 41
    F2 = 42
    F3 = 43
    F4 = 44
    F5 = 45
    F6 = 46

    def convertToMatrixIndices(self) -> tuple[int, int]:
        line = int(self.value) % 10 - 1
        col = int(self.value) // 10
        return (line, col)
    
    @staticmethod
    def from_input(day: str, value: str) -> Result['TimeInterval', str]:
        day_result = Day.from_string(day)
        interval_result = Interval.from_string(value)
        err = ""

        if not is_successful(day_result):
            err += day_result.failure()

        if not is_successful(interval_result):
            err += interval_result.failure()
        
        if err:
            return Failure(err)
        
        return Success(TimeInterval((day_result.unwrap().value[1] - 1) * 10 + interval_result.unwrap().value[1]))