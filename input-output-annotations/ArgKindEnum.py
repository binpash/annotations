from enum import Enum


class ArgKindEnum(Enum):
    FLAG = 1
    OPTION = 2
    OPERAND = 3
