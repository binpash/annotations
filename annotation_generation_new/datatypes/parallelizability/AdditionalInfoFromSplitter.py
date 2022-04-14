from enum import Enum

# this will probably become its own class with more information later
class AdditionalInfoFromSplitter(Enum):
    NO_ADD_INPUT = 'no_add_input'
    LINE_NUM_OFFSET = 'line_num_offset'
    BYTE_OFFSET = 'byte_offset'
    LINE_NUM_AND_BYTE_OFFSET = 'line_num_and_byte_offset'
