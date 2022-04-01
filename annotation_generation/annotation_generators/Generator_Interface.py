from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod

from datatypes.FlagOption import FlagOption
from datatypes.Operand import Operand
from datatypes.CommandInvocation import CommandInvocation

class Generator_Interface(ABC):

    # TODO: proper type for constructor of this super class
    def __init__(self, cmd_invocation: CommandInvocation) -> Generator_Interface:
        self.flag_option_list : List[FlagOption] = cmd_invocation.flag_option_list
        self.operand_list : List[Operand] = cmd_invocation.operand_list

    @abstractmethod
    def generate_info(self) -> None:
        pass

    @abstractmethod
    def get_info(self):
        pass

    ## HELPERS/Library functions: help to check conditions
    def get_operand_names_list(self) -> List[str]:
        return [operand.name for operand in self.operand_list]

    def does_flag_option_list_contains_at_least_one_of(self, list_names: List[str]) -> bool:
        return len(self.get_flag_option_list_filtered_with(list_names)) > 0

    def get_flag_option_list_filtered_with(self, list_names: List[str]) -> List[FlagOption]:
        return [flagoption for flagoption in self.flag_option_list if flagoption.get_name() in list_names]

