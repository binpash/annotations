from __future__ import annotations
from typing import Union, NewType

from datatypes.FileDescriptor import FileDescriptor

OptionArg = NewType('OptionArg', Union[str, FileDescriptor])

from abc import ABC


class FlagOption(ABC):

    def get_name(self) -> str:
        """get name of either option or flag"""


class Flag(FlagOption):

    def __init__(self, name: str) -> Flag:
        self.flag_name = name

    def __repr__(self) -> str:
        return self.flag_name

    def __eq__(self, other) -> bool:
        if isinstance(other, Flag):
            return self.flag_name == other.flag_name

    def get_name(self) -> str:
        return self.flag_name

class Option(FlagOption):

    def __init__(self, name: str, option_arg: OptionArg) -> Option:
        self.option_name = name
        self.option_arg = option_arg

    def __repr__(self) -> str:
        return self.option_name

    def __eq__(self, other) -> bool:
        if isinstance(other, Option):
            return self.option_name == other.option_name and self.option_arg == other.option_arg

    def get_name(self) -> str:
        return self.option_name
