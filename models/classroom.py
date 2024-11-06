from curses.ascii import isspace
from enum import Enum
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful

import models.constants as consts

class ClassroomType(Enum):
    LECTURE = 'Lecture'
    LABORATORY = 'Laboratory'
    INVALID = 'Invalid'

    @staticmethod
    def from_string(value: str) -> Result['ClassroomType', str]:
        try:
            return Success(ClassroomType(value))
        except ValueError:
            return Failure(f"Invalid classroom type {value}.\n")

class Classroom:
    """
    Represents a classroom model.
    
    This class encapsulates the attributes and behavior related to classrooms.

    .. Note::
        Direct instantiation of this class is not allowed. 
        
        Use the `create` method to instantiate a Classroom object.
    """

    __slots__ = '__id', '__type', 'availability'
    __id: str
    __type: ClassroomType
    availability: dict[consts.Day, list[str]]

    @staticmethod
    def create(id_: str, type_: str) -> Result["Classroom", str]:
        """
        Creates a Classroom object. In case of 
        an invalid type, or empty id it will return a error message.

        Parameters:
            id_ (str): Id of the classroom.
            type (str): Type of the classroom.
            
        Returns:
            Result: The object representing the classroom or a error message.
        """

        err = ''
        if not id_.strip():
            err += 'Id of the class cannot be empty.\n'
        
        resultType =  ClassroomType.from_string(type_)

        if not is_successful(resultType):
            err += resultType.failure()

        if err:
            return Failure(err)
        
        return Success(Classroom(id_, resultType.unwrap()))
    
    def __init__(self, id_: str, type: ClassroomType) -> None:
        """
        DO NOT USE THIS METHOD OUTSIDE the `Classroom` class.
        """

        self.__id = id_
        self.__type = type
        self.availability = consts.BASIC_AVAILABILITY

    def get_id(self) -> str:
        return self.__id
    
    def get_type(self) -> ClassroomType:
        return self.__type

    def __str__(self):
        availability_str = "\n".join([f"{day}: {', '.join(intervals)}" for day, intervals in self.availability.items()])

        return (
            f"Classroom: {self.__id}\n"
            f"Type: {self.__type.name}\n"
            f"Availability:\n{availability_str}"
        )
