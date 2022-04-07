from __future__ import annotations

from util import standard_eq, standard_repr

from datatypes.FileDescriptor import FileDescriptor

# OptionArgPosConfigType = NewType('OptionArgPosConfigType', Union[str, FileDescriptor])
StringType = str
OptionArgPosConfigType = StringType | FileDescriptor

from abc import ABC, abstractmethod


class FlagOption(ABC):

    @abstractmethod
    def get_name(self) -> str:
        """get name of either option or flag"""


class Flag(FlagOption):

    def __init__(self, name: str) -> None:
        self.flag_name = name

    def __repr__(self) -> str:
        return self.flag_name

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def get_name(self) -> str:
        return self.flag_name


class Option(FlagOption):

    def __init__(self, name: str, option_arg: OptionArgPosConfigType) -> None:
        self.option_name = name
        self.option_arg: OptionArgPosConfigType = option_arg

    def __repr__(self) -> str:
        return self.option_name

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def get_name(self) -> str:
        return self.option_name
