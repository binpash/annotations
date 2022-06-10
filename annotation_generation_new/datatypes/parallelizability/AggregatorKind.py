from enum import Enum

class AggregatorKindEnum(Enum):
    # Assumption: for multiple inputs, given in order of appearance: flagoption_list, operand_list
    # Assumption: for ADJ_LINES_* and CUSTOM_2_ARY, PaSh concatenates the resulting streams
    # Assumption: for ADJ_LINES_*, both lines are given in one input stream
    # Question: is this "streaming inputs" a resonable choice as condition for the command invocation?
    CONCATENATE = 1     # hard-coded;                   CommandInvocationWithIO with n streaming inputs (just operand list as cat) and 1 streaming output
    ADJ_LINES_MERGE = 2 # hard-coded;                   CommandInvocationWithIO with 1 streaming inputs and 1 streaming output
    ADJ_LINES_SEQ = 3   # hard-coded;                   CommandInvocationWithIO with 1 streaming inputs and 1 streaming output
    # should the function be a CommandInvocationWithIO itself?
    ADJ_LINES_FUNC = 4  # function for adjacent lines;  CommandInvocationWithIO with 1 streaming inputs and 1 streaming output
    CUSTOM_2_ARY = 5    # function for two inputs;      CommandInvocationWithIO with 2 streaming inputs and 1 streaming output
    CUSTOM_N_ARY = 6    # function for n inputs;        CommandInvocationWithIO with n streaming inputs and 1 streaming output
                                                            # How to know where to provide the n streaming inputs? One option or operand list?
