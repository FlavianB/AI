from typing import Optional

from returns.result import Result, Failure, Success

class Event:
    """
    Represents a event model.
    
    This class encapsulates the attributes and behavior related to an event.

    .. Note::
        Direct instantiation of this class is not allowed. 
        
        Use the `create` method to instantiate a Event object.
    """
      
    __slots__ = '__id', '__name', '__type', '__semester', '__optional_package', '__primary_instructors', '__secondary_instructors'
    __id: str
    __name: str
    __semester: int
    __optional_package: Optional[int] 
    
    __primary_instructors: list[int]
    __secondary_instructors: list[int]

    @staticmethod
    def create(name: str, semester: int, optional_package: Optional[int], 
               primary_instructors: list[int], secondary_instructors: list[int]) -> Result["Event", str]:
        """
        Creates a Event object. In case of 
        an invalid semester, invalid optional_package or empty instructors it will return a error message.

        Parameters:
            name (str): Name of the event.
            semester (str): An integer with values from 1 to 6.
            optional_package: An integer with values from 1 to 3.
            primary_instructors: A list of the ids of the instructors which can hold the lecture events.
            secondary_instructors: A list of the ids of the instructors which can hold the laboratory events.
            
        Returns:
            Result: The object representing the event or a error message.
        """

        err = ''
        if not name.strip():
            err += f'Name should not be empty'
        if (semester < 1 or semester > 6):
            err += f'Semester should be in interval 1-6, but has value {semester}.\n'
        if (optional_package is not None and (optional_package > 3 or optional_package < 1)):
            err += f"Optional should be in inverval 1-3 or None, but has value {optional_package}.\n"
        if len(primary_instructors) == 0:
            err += "There should exists primary instructors.\n"
        
        if err:
            return Failure(err)
        
        return Success(Event(name, semester, optional_package, primary_instructors, secondary_instructors))
    
    def __init__(self, name: str, semester: int, optional_package: Optional[int],
                 primary_instructors: list[int], secondary_instructors: list[int]):
        """
        DO NOT USE THIS METHOD OUTSIDE the `Classroom` class.
        """
        
        self.__id = f"{semester} {''.join(word[0].upper() for word in name.split() if word) if len(name.split(' ')) != 1 else name}"
        self.__name = name
        self.__semester = semester
        self.__optional_package = optional_package
        self.__primary_instructors = primary_instructors
        self.__secondary_instructors = secondary_instructors

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
            f"Year/Semester: {self.__semester // 2 + 1}/{self.__semester % 2 + 1}\n"
            f"Optional Package: {self.__optional_package}\n"
            f"Primary Instructors: {self.__primary_instructors}\n"
            f"Secondary Instructors: {self.__secondary_instructors}\n"
        )