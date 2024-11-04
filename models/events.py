from typing import Optional

# from returns.result import Result

class Event:
    __slots__ = '__id', '__name', '__type', '__semester', '__optional_package', '__primary_instructors', '__secondary_instructors'
    __id: str
    __name: str
    __semester: int
    __optional_package: Optional[int] # May have values from 1 - 3 (None means it's mandatory)
    __primary_instructors: list[int]
    __secondary_instructors: list[int]

    @staticmethod
    def create(name_: str, semester_: int, optional_package_: int, 
               primary_instructors_: list[int], secondary_instructors_: list[int]) -> "Event":
        clas = Event(name_, semester_, optional_package_)
        # Here should be a validation that the ids actually exists.
        # Needs to have the list of instructors available.
        # This function will also return a Result for this case.
        clas.__primary_instructors = primary_instructors_
        clas.__secondary_instructors = secondary_instructors_
        
        return clas
        
    def __init__(self, name: str, semester: int, optional_package: int):
        self.__id = f"{semester} {''.join(word[0].upper() for word in name.split() if word)}"
        self.__name = name
        self.__semester = semester
        self.__optional_package = optional_package
  

    def get_id(self) -> str:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_semester(self) -> int:
        return self.__semester

    def get_optional_package(self) -> Optional[int]:
        return self.__optional_package

    def get_primary_instructors(self) -> list[int]:
        return self.__primary_instructors

    def get_secondary_instructors(self) -> list[int]:
        return self.__secondary_instructors
    def __str__(self):
        return (
            f"Event: {self.__id}\n"
            f"Course: {self.__name}\n"
            f"Year/Semester: {self.__semester / 2 + 1}/{self.__semester % 2}\n"
            f"Optional Package: {self.__optional_package}\n"
            f"Primary Instructors: {self.__primary_instructors}\n"
            f"Secondary Instructors: {self.__secondary_instructors}\n"
        )