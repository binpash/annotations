from typing import List

from util_standard import standard_repr, standard_eq
from datatypes_new.BasicDatatypes import FlagOption, OptionArgPosConfigType

class CommandInvocationPrefix:

    def __init__(self, cmd_name: str, flag_option_list: List[FlagOption], positional_config_list: List[OptionArgPosConfigType]) -> None:
        self.cmd_name = cmd_name
        self.flag_option_list = flag_option_list
        self.positional_config_list = positional_config_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)
