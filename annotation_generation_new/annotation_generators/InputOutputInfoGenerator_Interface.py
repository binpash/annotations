from __future__ import annotations
from datatypes_new.CommandInvocationWithIOPartial import CommandInvocationWithIOPartial
from datatypes_new.CommandInvocationWithIOFull import CommandInvocationWithIOFull

from abc import ABC, abstractmethod

from annotation_generation_new.annotation_generators.Generator_Interface import Generator_Interface
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo


class InputOutputInfoGeneratorInterface(Generator_Interface, ABC):

    def __init__(self, cmd_invocation: CommandInvocationWithIOPartial) -> None:
        super().__init__(cmd_invocation=cmd_invocation)
        self.input_output_info: InputOutputInfo = InputOutputInfo(len(cmd_invocation.operand_list))

    @abstractmethod
    def generate_info(self) -> None:
        pass

    def get_info(self) -> InputOutputInfo:
        return self.input_output_info

    def get_augmented_cmd_inv(self) -> CommandInvocationWithIOFull:
        return self.input_output_info

    ## Library functions

    # use default values here as counter-measure for using False as default values in constructor

    def set_implicit_use_of_stdin(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdin(value)

    def set_implicit_use_of_stdout(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdout(value)

    # def set_multiple_inputs_possible(self, value: bool = True) -> None:
    #     self.input_output_info.set_multiple_inputs_possible(value)

    ## LIBRARY functions

    # TODO: remove, only used once, deprecated
    def get_length_ioinfo_positional_input_list(self) -> int:
        return 0

    def if_no_operands_given_stdin_implicitly_used(self) -> None:
        if len(self.operand_list) == 0:
            self.set_implicit_use_of_stdin(True)

    def if_version_or_help_stdout_implicitly_used(self) -> None:
        if self.is_version_or_help_in_flag_option_list():
            self.set_implicit_use_of_stdout()

    # forwarded to InputOutputInfo

    # Assumption: streaming inputs are always filenames or stdin
    # Assumption: (streaming) outputs are always filenames or stdout
    def all_operands_are_streaming_inputs(self) -> None:
        self.input_output_info.all_operands_are_streaming_inputs()

    def all_but_last_operand_is_streaming_input(self):
        self.input_output_info.all_but_last_operand_is_streaming_input()

    def all_but_last_operand_is_other_input(self):
        self.input_output_info.all_but_last_operand_is_other_input()

    def all_but_first_operand_is_streaming_input(self):
        self.input_output_info.all_but_first_operand_is_streaming_input()

    def all_but_first_operand_is_other_input(self):
        self.input_output_info.all_but_first_operand_is_other_input()

    def only_last_operand_is_output(self):
        self.input_output_info.only_last_operand_is_output()

    def set_all_operands_as_positional_config_arg_type_string(self):
        self.input_output_info.set_all_operands_as_positional_config_arg_type_string()

    def set_first_operand_as_positional_config_arg_type_string(self):
        self.input_output_info.set_first_operand_as_positional_config_arg_type_string()

    def set_first_operand_as_positional_config_arg_type_filename_or_std_descriptor(self):
        self.input_output_info.set_first_operand_as_positional_config_arg_type_filename_or_std_descriptor()
