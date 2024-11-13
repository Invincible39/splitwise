from enum import Enum

class SplitTypeEnum(str, Enum):
    """
    Enum for Pydantic models to ensure consistent split types.
    """
    EQUAL = 'equal'
    PERCENTAGE = 'percentage'
    UNEQUAL = 'unequal'
