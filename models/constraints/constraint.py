from models.constraints.constants import ConstraintType, Weight


class Constraint:
    __slots__ = '__weight', '__type'
    __weight: Weight
    __type: ConstraintType

    def __init__(self, type: ConstraintType, weight: Weight):
        self.__type = type
        self.__weight = weight
    
    def get_weight(self) -> Weight:
       return self.__weight
    
    def get_type(self) -> ConstraintType:
        return self.__type