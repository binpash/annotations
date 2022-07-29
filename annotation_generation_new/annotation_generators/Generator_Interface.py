from typing import List
from abc import ABC, abstractmethod

from datatypes_new.BasicDatatypes import FlagOption
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial

class Generator_Interface(ABC):

    def __init__(self, cmd_invocation: CommandInvocationInitial) -> None:
        self.cmd_inv: CommandInvocationInitial = cmd_invocation

    @abstractmethod
    def generate_info(self) -> None:
        pass

    @abstractmethod
    def get_info(self):
        pass

    ## HELPERS/Library functions: to check conditions

    def does_flag_option_list_contain_at_least_one_of(self, list_names: List[str]) -> bool:
        return len(self.get_flag_option_list_filtered_with(list_names)) > 0

    def get_flag_option_list_filtered_with(self, list_names: List[str]) -> List[FlagOption]:
        return [flagoption for flagoption in self.cmd_inv.flag_option_list if flagoption.get_name() in list_names]

    def get_operand_list_length(self):
        return len(self.cmd_inv.operand_list)

    def get_first_operand_name_as_string(self):
        # assumes that it is of type config
        first_operand = self.cmd_inv.operand_list[0]
        first_operand_arg = first_operand.get_name()
        first_operand_name = str(first_operand_arg)
        return first_operand_name

    def does_first_operand_start_with(self, arg):
        first_operand_name = self.get_first_operand_name_as_string()
        return first_operand_name.startswith(arg)

    def does_first_operand_contain(self, arg):
        first_operand_name = self.get_first_operand_name_as_string()
        return (arg in first_operand_name)
