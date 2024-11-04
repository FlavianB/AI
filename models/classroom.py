from enum import Enum
from returns.result import Result, Success, Failure

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
            return Failure(f"Invalid classroom type {value}")

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
        an invalid type, it will return an object with the field `type`
        equal to `ClassroomType.INVALID`.

        Parameters:
            id_ (str): Id of the classroom.
            type_ (str): Type of the classroom.
            
        Returns:
            Classroom: The object representing the classroom.
        """
        clas = Classroom(id_)
        clas.__id = id_
        resultType =  ClassroomType.from_string(type_)
        match resultType:
            case Success(type):
                clas.__type = type
            case Failure(err):
                return Failure(err) 
        
        clas.availability = consts.BASIC_AVAILABILITY.copy()
        return Success(clas)

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
    
    def __init__(self, id_: str) -> None:
        """
        DO NOT USE THIS METHOD OUTSIDE the `Classroom` class.
        """
        self.__id = id_
        self.availability = consts.BASIC_AVAILABILITY
