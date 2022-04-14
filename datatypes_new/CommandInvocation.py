from __future__ import annotations
from typing import List

from datatypes_new.BasicDatatypes import FlagOption, Operand
from util_standard import standard_repr, standard_eq

class CommandInvocation:

    def __init__(self, cmd_name: str, flag_option_list: List[FlagOption], operand_list: List[Operand]) -> None:
        self.cmd_name = cmd_name
        self.flag_option_list = flag_option_list
        self.operand_list = operand_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other: CommandInvocation):
        return standard_eq(self, other)
