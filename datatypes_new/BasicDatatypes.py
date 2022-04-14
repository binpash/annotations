from __future__ import annotations
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

class StdDescriptor(BaseClassForBasicDatatypes):

    def __init__(self, name: StdDescriptorEnum) -> None:
        # name should be a number
        self.name = name

    def get_name(self) -> str:
        return str(self.name)

    @staticmethod
    def get_stdin_fd() -> StdDescriptor:
        return StdDescriptor(StdDescriptorEnum.STDIN)

    @staticmethod
    def get_stdout_fd() -> StdDescriptor:
        return StdDescriptor(StdDescriptorEnum.STDOUT)

    @staticmethod
    def get_stderr_fd() -> StdDescriptor:
        return StdDescriptor(StdDescriptorEnum.STDERR)

class StdDescriptorEnum(Enum):
    STDIN = 0
    STDOUT = 1
    STDERR = 2

FileDescriptor = Union[FileName, StdDescriptor]

class ArgStringType(BaseClassForBasicDatatypes):

    def __init__(self, name: str) -> None:
        self.name = name

    def get_name(self) -> str:
        return self.name

OptionArgPosConfigType = Union[ArgStringType, FileDescriptor]

class Flag(BaseClassForBasicDatatypes):

    def __init__(self, name: str) -> None:
        self.flag_name = name

    def get_name(self) -> str:
        return self.flag_name


class Option(BaseClassForBasicDatatypes):

    def __init__(self, name: str, option_arg: OptionArgPosConfigType) -> None:
        self.option_name = name
        self.option_arg: OptionArgPosConfigType = option_arg

    def get_name(self) -> str:
        return self.option_name

FlagOption = Union[Flag, Option]

class Operand(BaseClassForBasicDatatypes):

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{self.name}'

    def get_name(self) -> str:
        return self.name

    def contains(self, arg):
        return self.name.__contains__(arg)

    def to_arg_string_type(self):
        return ArgStringType(self.name)
