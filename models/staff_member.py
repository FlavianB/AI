from enum import Enum
from typing import Dict, List
import numpy as np
from returns.result import Result, Success, Failure
from returns.pipeline import is_successful
import models.constants as consts

class StaffMemberPosition(Enum):
    ASSISTANT = 'Assistant'
    LECTURER = 'Lecturer'
    CONF = 'Conf'
    INVALID = 'Invalid'
    
    @staticmethod
    def from_string(value: str) -> Result['StaffMemberPosition', str]:
        try:
            return Success(StaffMemberPosition(value))
        except ValueError:
            return Failure(f"Invalid staff member position '{value}'.\n")

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
    availability: np.ndarray

    @staticmethod
    def create(id_: str, position: str, name: str) -> Result["StaffMember", str]:
        """
        Creates a StaffMember object with validation. Returns a Failure if any validation fails.

        Parameters:
            id_ (str): Unique ID of the staff member.
            position (str): Position of the staff member.
            name (str): Name of the staff member (first and last name).
            
        Returns:
            Result: A `Success` with the created object or a `Failure` with an error message.
        """
        
        err = ""
        if not id_.strip():
            err += "ID cannot be empty.\n"
        
        if not name.strip():
            err += "The name must not be empty.\n"
        
        staff_member = StaffMember(id_)

        position_result = StaffMemberPosition.from_string(position)
        if not is_successful(position_result):
            err += position_result.failure()
        else:
            staff_member.__position = position_result.unwrap()

        if err:
            return Failure(err)
        
        staff_member.__id = id_
        staff_member.__name = name
        staff_member.availability = consts.BASIC_AVAILABILITY.copy()

        return Success(staff_member)

    def get_id(self) -> str:
        return self.__id
    
    def get_position(self) -> StaffMemberPosition:
        return self.__position
    
    def get_name(self) -> str:
        return self.__name

    def __str__(self):
        availability_str = "\n".join([f"{day}: {', '.join(day)}" for day in self.availability])
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
