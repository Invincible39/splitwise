import enum

class SplitTypeEnum(str, enum.Enum):
    EQUAL = 'equal'
    PERCENTAGE = 'percentage'
    UNEQUAL = 'unequal'
