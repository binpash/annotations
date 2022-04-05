from __future__ import annotations
from typing import List

from util import standard_repr, standard_eq
from datatypes.FlagOption import FlagOption, OptionArgPosConfigType

class CommandInvocationPrefix:

    def __init__(self, cmd_name: str, flag_option_list: List[FlagOption], positional_config_list: List[OptionArgPosConfigType]) -> None:
        self.cmd_name = cmd_name
        self.flag_option_list = flag_option_list
        self.positional_config_list = positional_config_list

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other: CommandInvocationPrefix):
        return standard_eq(self, other)
