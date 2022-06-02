from __future__ import annotations
from typing import List, Union

from datatypes_new.BasicDatatypes import FlagOption, ArgStringType
from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameOrStdDescriptorWithIOInfo
from util_standard import standard_repr, standard_eq

class CommandInvocationWithIOFull:

    def __init__(self, cmd_name: str,
                 flag_option_list: List[Union[FlagOption, OptionWithIO]],
                 operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                 implicit_use_of_stdin: bool,
                 implicit_use_of_stdout: bool
                 ) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[Union[FlagOption, OptionWithIO]] = flag_option_list
        self.operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]] = operand_list
        self.implicit_use_of_stdin: bool = implicit_use_of_stdin
        self.implicit_use_of_stdout: bool = implicit_use_of_stdout

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other: CommandInvocationWithIOFull):
        return standard_eq(self, other)
