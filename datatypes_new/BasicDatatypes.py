from typing import Union

from util_standard import standard_eq, standard_repr

from enum import Enum

from abc import ABC, abstractmethod

# note that we have individual classes since aliasing does not provide as much support
class BaseClassForBasicDatatypes(ABC):

    def __repr__(self) -> str:
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    @abstractmethod
    def get_name(self) -> str:
        pass

class FileName(BaseClassForBasicDatatypes):

    def __init__(self, name: str) -> None:
        # name should be a string
        self.name = name

    def get_name(self) -> str:
        return self.name

class StdDescriptorEnum(Enum):
    STDIN = 0
    STDOUT = 1
    STDERR = 2

class StdDescriptor(BaseClassForBasicDatatypes):

    def __init__(self, name: StdDescriptorEnum) -> None:
        # name should be a number
        self.name = name

    def get_name(self) -> str:
        return str(self.name)

    def get_type(self) -> StdDescriptorEnum:
        return self.name

def get_stdin_fd() -> StdDescriptor:
    return StdDescriptor(StdDescriptorEnum.STDIN)

def get_stdout_fd() -> StdDescriptor:
    return StdDescriptor(StdDescriptorEnum.STDOUT)

def get_stderr_fd() -> StdDescriptor:
    return StdDescriptor(StdDescriptorEnum.STDERR)

FileNameOrStdDescriptor = Union[FileName, StdDescriptor]

class ArgStringType(BaseClassForBasicDatatypes):

    def __init__(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

OptionArgPosConfigType = Union[ArgStringType, FileNameOrStdDescriptor]

class Flag(BaseClassForBasicDatatypes):

    def __init__(self, name: str) -> None:
        self.flag_name = name

    def get_name(self) -> str:
        return self.flag_name


class Option(BaseClassForBasicDatatypes):

    def __init__(self, name: str, option_arg: str) -> None:
        self.option_name = name
        self.option_arg: str = option_arg

    def get_name(self) -> str:
        return self.option_name

    def get_arg(self) -> str:
        return self.option_arg

    # def is_arg_of_type_string(self):
    #     return isinstance(self.option_arg, ArgStringType)
    #
    # def is_arg_of_type_filename_or_stddescriptor(self):
    #     return isinstance(self.option_arg, FileName) or isinstance(self.option_arg, StdDescriptor)

FlagOption = Union[Flag, Option]

# Note difference between Option argument and Operand after parsing:
# for option arguments, we know which is a filename; for operands, we don't

class Operand(BaseClassForBasicDatatypes):

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{self.name}'

    def get_name(self) -> str:
        return self.name

    def contains_new_line(self):
        name_as_string = str(self.name)
        return name_as_string.find(r"\n") > 0

    def contains_null_char(self):
        name_as_string = str(self.name)
        return name_as_string.find(r"\0") > 0

    def to_arg_string_type(self):
        return ArgStringType(self.name)


class WhichClassForArg(Enum):
    FILESTD = 'filestd'
    ARGSTRING = 'argstring'
    PLAINSTRING = 'str'

# copied from ir_utils
def format_arg_chars(arg_chars):
    chars = [format_arg_char(arg_char) for arg_char in arg_chars]
    return "".join(chars)

##
## BIG TODO: Fix the formating of arg_chars bask to shell scripts and string.
##           We need to do this the proper way using the parser.
##
def format_arg_char(arg_char):
    key, val = get_kv(arg_char)
    if (key == 'C'):
        return str(chr(val))
    elif (key == 'B'):
        # The $() is just for illustration. This is backticks
        return '$({})'.format(val)
    elif (key == 'Q'):
        formated_val = format_arg_chars(val)
        return '"{}"'.format(formated_val)
    elif (key == 'V'):
        return '${{{}}}'.format(val[2])
    elif (key == 'E'):
        ## TODO: This is not right. I think the main reason for the
        ## problems is the differences between bash and the posix
        ## standard.
        # log(" -- escape-debug -- ", val, chr(val))
        non_escape_chars = [92, # \
                            61, # =
                            91, # [
                            93, # ]
                            45, # -
                            58, # :
                            126,# ~
                            42] # *
        if(val in non_escape_chars):
            return '{}'.format(chr(val))
        else:
            return '\{}'.format(chr(val))
    else:
        # log("Cannot format arg_char:", arg_char)
        ## TODO: Make this correct
        raise NotImplementedError


## This function gets a key and a value from the ast json format
def get_kv(dic):
    return (dic[0], dic[1])
