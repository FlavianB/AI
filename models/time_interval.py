from enum import Enum

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
    M1 = 1,
    M2 = 2,
    M3 = 3,
    M4 = 4,
    M5 = 5,
    M6 = 6,

    T1 = 11,
    T2 = 12,
    T3 = 13,
    T4 = 14,
    T5 = 15,
    T6 = 16,

    W1 = 21,
    W2 = 22,
    W3 = 23,
    W4 = 24,
    W5 = 25,
    W6 = 26,

    TH1 = 31,
    TH2 = 32,
    TH3 = 33,
    TH4 = 34,
    TH5 = 35,
    TH6 = 36,

    F1 = 41,
    F2 = 42,
    F3 = 43,
    F4 = 44,
    F5 = 45,
    F6 = 46,
