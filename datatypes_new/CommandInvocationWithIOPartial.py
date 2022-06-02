from __future__ import annotations
from typing import List, Union

from datatypes_new.BasicDatatypes import FlagOption, ArgStringType
from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameOrStdDescriptorWithIOInfo
from util_standard import standard_repr, standard_eq

class CommandInvocationWithIOPartial:

    def __init__(self, cmd_name: str,
                 flag_option_list: List[Union[FlagOption, OptionWithIO]],
                 operand_list: List[ArgStringType]
                 ) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[Union[FlagOption, OptionWithIO]] = flag_option_list
        self.operand_list: List[ArgStringType] = operand_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other: CommandInvocationWithIOPartial):
        return standard_eq(self, other)
