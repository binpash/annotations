from typing import List

from datatypes_new.BasicDatatypes import FlagOption, Operand
from util_standard import standard_repr, standard_eq

class CommandInvocationInitial:

    def __init__(self, cmd_name: str, flag_option_list: List[FlagOption], operand_list: List[Operand]) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[FlagOption] = flag_option_list
        self.operand_list: List[Operand] = operand_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)
