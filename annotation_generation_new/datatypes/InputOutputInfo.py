from __future__ import annotations
from util_standard import standard_repr
from typing import List, Tuple, Union
from datatypes_new.AccessKind import AccessKind
from datatypes_new.CommandInvocationWithIOPartial import CommandInvocationWithIOPartial
from datatypes_new.CommandInvocationWithIOFull import CommandInvocationWithIOFull
from datatypes_new.BasicDatatypes import Operand, ArgStringType, FileNameOrStdDescriptor, FileName, StdDescriptor
from datatypes_new.BasicDatatypesWithIO import FileNameOrStdDescriptorWithIOInfo, FileNameWithIOInfo, StdDescriptorWithIOInfo
from util_new import compute_actual_el_for_input, compute_actual_el_for_output

class InputOutputInfo:

    def __init__(self,
                 number_of_operands : int,
                 implicit_use_of_stdin : bool = False,
                 implicit_use_of_stdout : bool = False,
                 ) -> None:
        self.operand_list_typer: List[Tuple[bool, AccessKind]] = [(True, AccessKind.make_stream_input()) ] * number_of_operands
            # defaults to FileName/StdDescriptor as Stream Input
            # bool indicates whether to interpret as ArgStringType (False) or as FileName/StdDescriptor (True)
            # this is later applied to CMDInvPartial to obtain CmdInvFull and we compute correct StdDescriptor with AccessKind
        self.implicit_use_of_stdin : bool = implicit_use_of_stdin
        self.implicit_use_of_stdout : bool = implicit_use_of_stdout

    def __repr__(self) -> str:
        return standard_repr(self)

    # Assumption: for operand_list_types, we assume no double assignment

    def set_implicit_use_of_stdin(self, value: bool) -> None:
        self.implicit_use_of_stdin = value

    def set_implicit_use_of_stdout(self, value: bool) -> None:
        self.implicit_use_of_stdout = value

    def all_operands_are_streaming_inputs(self) -> None:
        pass # since this is the default in the constructor

    def all_but_last_operand_is_streaming_input(self):
        pass # since this is the default in the constructor and we assume the last is assigned somewhere else

    def all_but_last_operand_is_other_input(self):
        original_last_entry = self.operand_list_typer[-1]
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(False, AccessKind.make_other_input())] * number_of_operands
        self.operand_list_typer[-1] = original_last_entry

    def all_but_first_operand_is_streaming_input(self):
        pass # since this is the default in the constructor and we assume the last is assigned somewhere else

    def all_but_first_operand_is_other_input(self):
        original_first_entry = self.operand_list_typer[0]
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(False, AccessKind.make_other_input())] * number_of_operands
        self.operand_list_typer[0] = original_first_entry


    def only_last_operand_is_output(self):
        self.operand_list_typer[-1] = (True, AccessKind.make_output())

    def set_all_operands_as_positional_config_arg_type_string(self):
        number_of_operands = len(self.operand_list_typer)
        self.operand_list_typer = [(False, AccessKind.make_conf_input())] * number_of_operands

    def set_first_operand_as_positional_config_arg_type_string(self):
        self.operand_list_typer[0] = (False, AccessKind.make_conf_input())

    def set_first_operand_as_positional_config_arg_type_filename_or_std_descriptor(self):
        self.operand_list_typer[0] = (True, AccessKind.make_conf_input())

    # TODO: adapt use in PaSh
    # def unpack_info(self) \
    #     -> Tuple[List[OptionArgPosConfigType], List[FileNameOrStdDescriptor], List[FileNameOrStdDescriptor], bool, bool, bool]:
    #     return self.positional_config_list, self.positional_input_list, self.positional_output_list, \
    #              self.implicit_use_of_stdin, self.implicit_use_of_stdout, self.multiple_inputs_possible

    def apply_input_output_info_to_command_invocation_with_IO_partial(
            self,
            cmd_inv_io_partial: CommandInvocationWithIOPartial
        ) -> CommandInvocationWithIOFull:
        operand_list_original: List[Operand] = cmd_inv_io_partial.operand_list
        operand_list_with_io_full: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]] = \
            [InputOutputInfo.apply_typer_to_operand(operand, typer) for (operand, typer) in zip(operand_list_original, self.operand_list_typer)]
        cmd_inv_io_full = CommandInvocationWithIOFull(
            cmd_name=cmd_inv_io_partial.cmd_name,
            flag_option_list=cmd_inv_io_partial.flag_option_list,
            operand_list=operand_list_with_io_full,
            implicit_use_of_stdin=self.implicit_use_of_stdin,
            implicit_use_of_stdout=self.implicit_use_of_stdout
        )
        return cmd_inv_io_full

    @staticmethod
    def apply_typer_to_operand(operand: Operand, typer: Tuple[bool, AccessKind]) \
        -> Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]:
        interpret_as_filename_or_stddescriptor, access = typer
        if interpret_as_filename_or_stddescriptor:
            if access.is_any_input():
                filename_or_stddescriptor: FileNameOrStdDescriptor = compute_actual_el_for_input(operand)
            elif access.is_output():
                filename_or_stddescriptor: FileNameOrStdDescriptor = compute_actual_el_for_output(operand)
            else:
                raise Exception("access which is neither any input nor ouput")
            if isinstance(filename_or_stddescriptor, FileName):
                return FileNameWithIOInfo.get_from_original(filename_or_stddescriptor, access)
            elif isinstance(filename_or_stddescriptor, StdDescriptor):
                return StdDescriptorWithIOInfo.get_from_original(filename_or_stddescriptor, access)
        else: # interpret as string
            return ArgStringType(operand.get_name())
