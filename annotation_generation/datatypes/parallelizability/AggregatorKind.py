from enum import Enum

class AggregatorKindEnum(Enum):
    CONCATENATE = 1
    ADJ_LINES_MERGE = 2
    ADJ_LINES_SEQ = 3
    ADJ_LINES_FUNC = 4
    CUSTOM_2_ARY = 5
    CUSTOM_N_ARY = 6
