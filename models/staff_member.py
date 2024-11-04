from enum import Enum

import models.constants as consts

class StaffMemberPosition(Enum):
    PROFESSOR = 'Professor'
    ASSISTANT = 'Assistant'
    INVALID = 'Invalid'

    @staticmethod
    def from_string(value: str) -> 'StaffMemberPosition':
        try:
            return StaffMemberPosition(value)
        except ValueError:
            return StaffMemberPosition.INVALID

class StaffMember:
    """
    Represents a staff member model.
    
    This class encapsulates the attributes and behavior related to staff members.

    .. Note::
        Direct instantiation of this class is not allowed. 
        
        Use the `create` method to instantiate a StaffMember object.
    """
    __slots__ = '__id', '__position', '__name', 'availability'
    __id: str
    __position: StaffMemberPosition
    __name: str
    availability: dict[consts.Day, list[str]]

    @staticmethod
    def create(id_: str, position_: str, name_: str) -> "StaffMember":
        """
        Creates a StaffMember object. In case of 
        an invalid position, it will return an object with the field `position`
        equal to `StaffMemberPosition.INVALID`.

        Parameters:
            id_ (str): Id of the classroom.
            position_ (str): Position of the classroom.
            name_ (str): Name of the staff member (first and last name)
            
        Returns:
            StaffMember: The object representing the classroom.
        """
        clas = StaffMember(id_)
        clas.__id = id_
        clas.__name = name_
        clas.__position = StaffMemberPosition.from_string(position_)
        clas.availability = consts.BASIC_AVAILABILITY
        return clas

    def get_id(self) -> str:
        return self.__id
    
    def get_position(self) -> StaffMemberPosition:
        return self.__position
    
    def get_name(self) -> str:
        return self.__name

    def __str__(self):
        availability_str = "\n".join([f"{day}: {', '.join(intervals)}" for day, intervals in self.availability.items()])
        return (
            f"StaffMember: {self.__id}\n"
            f"Position: {self.__position.name}\n"
            f"Name: {self.__name}\n"
            f"Availability:\n{availability_str}"
        )
    
    def __init__(self, id_: str) -> None:
        """
        DO NOT USE THIS METHOD OUTSIDE the `StaffMember` class.
        """
        self.__id = id_
        self.availability = consts.BASIC_AVAILABILITY
