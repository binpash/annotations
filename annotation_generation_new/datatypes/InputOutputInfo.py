from __future__ import annotations

from util_standard import standard_repr
from typing import List, Tuple, Union, Optional
from datatypes_new.AccessKind import AccessKind
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.BasicDatatypes import Operand, ArgStringType, FileNameOrStdDescriptor, FileName, StdDescriptor, \
    FlagOption
from datatypes_new.BasicDatatypesWithIO import FileNameOrStdDescriptorWithIOInfo, FileNameWithIOInfo, \
    StdDescriptorWithIOInfo, OptionWithIO
from util_new import compute_actual_el_for_input, compute_actual_el_for_output

class InputOutputInfo:

    def __init__(self,
                 flagoption_list_typer : List[Tuple[bool, Optional[AccessKind]]],
                 number_of_operands : int,
                 implicit_use_of_streaming_input : Optional[FileNameOrStdDescriptorWithIOInfo] = None,
                 implicit_use_of_streaming_output : Optional[FileNameOrStdDescriptorWithIOInfo] = None,
                 ) -> None:
        self.flagoption_list_typer: List[Tuple[bool, Optional[AccessKind]]] = flagoption_list_typer
        self.operand_list_typer: List[Tuple[bool, AccessKind]] = [(True, AccessKind.make_stream_input()) ] * number_of_operands
            # defaults to FileName/StdDescriptor as Stream Input
            # bool indicates whether to interpret as ArgStringType (False) or as FileName/StdDescriptor (True)
            # this is later applied to CMDInvPartial to obtain CmdInvFull and we compute correct StdDescriptor with AccessKind
        self.implicit_use_of_streaming_input : Optional[FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_input
        self.implicit_use_of_streaming_output : Optional[FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_output

    def __repr__(self) -> str:
        return standard_repr(self)

    # the InputOutputInfoGenerator Interface automatically calls this function to set this
    def set_typer_for_flagoptions(self, list_typer_for_flagoptions):
        self.flagoption_list_typer = list_typer_for_flagoptions

    # Assumption: for operand_list_types, we assume no double assignment

    def set_implicit_use_of_stdin(self, value: bool) -> None:
        if value:
            stdin_with_io = StdDescriptorWithIOInfo.get_from_original(StdDescriptor.get_stdin_fd(), AccessKind.make_stream_input())
            self.set_implicit_use_of_streaming_input(stdin_with_io)
        else:
            pass # since default value is None anyway

    def set_implicit_use_of_streaming_input(self, implicit_input: Optional[FileNameOrStdDescriptorWithIOInfo]) -> None:
        self.implicit_use_of_streaming_input = implicit_input

    def set_implicit_use_of_stdout(self, value: bool) -> None:
        if value:
            stdout_with_io = StdDescriptorWithIOInfo.get_from_original(StdDescriptor.get_stdout_fd(), AccessKind.make_stream_output())
            self.set_implicit_use_of_streaming_output(stdout_with_io)
        else:
            pass # since default value is None anyway

    def set_implicit_use_of_streaming_output(self, implicit_output: Optional[FileNameOrStdDescriptorWithIOInfo]) -> None:
        self.implicit_use_of_streaming_output = implicit_output

    def all_operands_are_streaming_inputs(self) -> None:
        pass # since this is the default in the constructor

    def all_operands_are_other_inputs(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(True, AccessKind.make_other_input())] * number_of_operands

    def all_but_last_operand_is_streaming_input(self) -> None:
        pass # since this is the default in the constructor and we assume the last is assigned somewhere else

    def all_but_last_operand_is_other_input(self) -> None:
        original_last_entry = self.operand_list_typer[-1]
        self.all_operands_are_other_inputs()
        self.operand_list_typer[-1] = original_last_entry

    def all_but_first_operand_is_streaming_input(self) -> None:
        pass # since this is the default in the constructor and we assume the last is assigned somewhere else

    def all_but_first_operand_is_other_input(self) -> None:
        original_first_entry = self.operand_list_typer[0]
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(False, AccessKind.make_other_input())] * number_of_operands
        self.operand_list_typer[0] = original_first_entry

    def only_last_operand_is_stream_output(self) -> None:
        self.operand_list_typer[-1] = (True, AccessKind.make_stream_output())

    def only_last_operand_is_other_output(self) -> None:
        self.operand_list_typer[-1] = (True, AccessKind.make_other_output())

    def set_all_operands_as_positional_config_arg_type_string(self) -> None:
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(False, AccessKind.make_config_input())] * number_of_operands

    def set_first_operand_as_positional_config_arg_type_string(self) -> None:
        self.operand_list_typer[0] = (False, AccessKind.make_config_input())

    def set_first_operand_as_positional_config_arg_type_filename_or_std_descriptor(self) -> None:
        self.operand_list_typer[0] = (True, AccessKind.make_config_input())


    # TODO: adapt use in PaSh
    # def unpack_info(self) \
    #     -> Tuple[List[OptionArgPosConfigType], List[FileNameOrStdDescriptor], List[FileNameOrStdDescriptor], bool, bool, bool]:
    #     return self.positional_config_list, self.positional_input_list, self.positional_output_list, \
    #              self.implicit_use_of_stdin, self.implicit_use_of_stdout, self.multiple_inputs_possible

    def apply_input_output_info_to_command_invocation(self, cmd_inv: CommandInvocationInitial) \
        -> CommandInvocationWithIO:
        # 1) transform flagoption list
        flagoption_list_original: List[FlagOption] = cmd_inv.flag_option_list
        # TODO
        flagoption_list_with_io: List[Union[FlagOption, OptionWithIO]] = []
        # 2) transform operand list
        operand_list_original: List[Operand] = cmd_inv.operand_list
        operand_list_with_io_full: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]] = \
            [InputOutputInfo.apply_typer_to_operand(operand, typer) for (operand, typer) in zip(operand_list_original, self.operand_list_typer)]
        # 3) build the command invocation with io and return
        cmd_inv_io_full = CommandInvocationWithIO(
            cmd_name=cmd_inv.cmd_name,
            flag_option_list=flagoption_list_with_io,
            operand_list=operand_list_with_io_full,
            implicit_use_of_streaming_input=self.implicit_use_of_streaming_input,
            implicit_use_of_streaming_output=self.implicit_use_of_streaming_output
        )
        return cmd_inv_io_full

    @staticmethod
    def apply_typer_to_operand(operand: Operand, typer: Tuple[bool, AccessKind]) \
        -> Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]:
        interpret_as_filename_or_stddescriptor, access = typer
        if interpret_as_filename_or_stddescriptor:
            if access.is_any_input():
                filename_or_stddescriptor: FileNameOrStdDescriptor = compute_actual_el_for_input(operand)
            elif access.is_any_output():
                filename_or_stddescriptor: FileNameOrStdDescriptor = compute_actual_el_for_output(operand)
            else:
                print(access)
                raise Exception("access which is neither any input nor output")
            if isinstance(filename_or_stddescriptor, FileName):
                return FileNameWithIOInfo.get_from_original(filename_or_stddescriptor, access)
            elif isinstance(filename_or_stddescriptor, StdDescriptor):
                return StdDescriptorWithIOInfo.get_from_original(filename_or_stddescriptor, access)
        else: # interpret as string
            return ArgStringType(operand.get_name())