from __future__ import annotations
from typing import Optional, List

from util_standard import standard_repr, standard_eq
from util_new import return_empty_flag_option_list_if_none_else_itself, return_empty_pos_config_list_if_none_else_itself

from datatypes_new.BasicDatatypes import FlagOption, OptionArgPosConfigType
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix

class Mapper:

    def __init__(self,
                 cmd_name: str,
                 flag_option_list : Optional[List[FlagOption]] = None,  # None translates to empty list
                 positional_config_list : Optional[List[OptionArgPosConfigType]] = None,  # None translates to empty list
                 num_outputs : int = 1
                 ) -> None:
        # for now, we also store if the mapper is the same to handle the cases similarly
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[FlagOption] = return_empty_flag_option_list_if_none_else_itself(flag_option_list)
        self.positional_config_list: List[OptionArgPosConfigType] = return_empty_pos_config_list_if_none_else_itself(positional_config_list)
        self.num_outputs : int = num_outputs

    def __eq__(self, other: Mapper) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    @staticmethod
    def make_mapper_from_command_invocation_prefix(command_invocation_prefix: CommandInvocationPrefix):
        return Mapper(command_invocation_prefix.cmd_name,
                      command_invocation_prefix.flag_option_list,
                      command_invocation_prefix.positional_config_list)
