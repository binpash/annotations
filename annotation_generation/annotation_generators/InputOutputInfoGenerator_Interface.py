from __future__ import annotations
from typing import List
from datatypes.BasicDatatypes import OptionArgPosConfigType, Operand

from abc import ABC, abstractmethod

from annotation_generation.annotation_generators.Generator_Interface import Generator_Interface
from datatypes.CommandInvocation import CommandInvocation
from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation.util import compute_actual_el_for_input


class InputOutputInfoGeneratorInterface(Generator_Interface, ABC):

    def __init__(self, cmd_invocation: CommandInvocation) -> None:
        super().__init__(cmd_invocation=cmd_invocation)
        self.input_output_info: InputOutputInfo = InputOutputInfo()

    @abstractmethod
    def generate_info(self) -> None:
        pass

    def get_info(self) -> InputOutputInfo:
        return self.input_output_info

    ## Member attributes only changed through these functions

    def set_ioinfo_positional_config_list(self, value: List[OptionArgPosConfigType]) -> None:
        self.input_output_info.set_positional_config_list(value)

    def set_ioinfo_positional_input_list(self, value: List[Operand]) -> None:
        self.input_output_info.set_positional_input_list(value)

    def set_ioinfo_positional_output_list(self, value: List[Operand]) -> None:
        self.input_output_info.set_positional_output_list(value)

    ## Library functions

    # use default values here as counter-measure for using False as default values in constructor

    def set_implicit_use_of_stdin(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdin(value)

    def set_implicit_use_of_stdout(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdout(value)

    def set_multiple_inputs_possible(self, value: bool = True) -> None:
        self.input_output_info.set_multiple_inputs_possible(value)

    # Library functions

    def get_length_ioinfo_positional_input_list(self) -> int:
        return len(self.input_output_info.positional_input_list)

    def if_no_operands_given_stdin_implicitly_used(self) -> None:
        if len(self.operand_list) == 0:
            self.set_implicit_use_of_stdin(True)

    def all_operands_are_inputs(self) -> None:
        self.set_ioinfo_positional_input_list(self.operand_list)

    def if_version_or_help_stdout_implicitly_used(self) -> None:
        if self.is_version_or_help_in_flag_option_list():
            self.set_implicit_use_of_stdout()

    def all_but_last_operand_is_input(self):
        self.set_ioinfo_positional_input_list(self.operand_list[:-1])

    def all_but_first_operand_is_input(self):
        self.set_ioinfo_positional_input_list(self.operand_list[1:])

    def only_last_operand_is_output(self):
        self.set_ioinfo_positional_output_list(self.operand_list[-1:])

    def set_first_operand_as_positional_config_arg_type_string(self):
        # type actual List[StringType] but pyright cannot do the cast for the variable
        pos_config_list: List[OptionArgPosConfigType] = [operand.to_arg_string_type() for operand in self.operand_list[:1]]
        self.set_ioinfo_positional_config_list(pos_config_list)

    def set_first_operand_as_positional_config_arg_type_filedescriptor(self):
        # type actual List[FileDescriptor] but pyright cannot do the cast for the variable
        pos_config_list: List[OptionArgPosConfigType] = [compute_actual_el_for_input(operand) for operand in self.operand_list[:1]]
        self.set_ioinfo_positional_config_list(pos_config_list)
