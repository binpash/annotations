from __future__ import annotations
from typing import List, Union, Optional, Tuple

from datatypes_new.BasicDatatypes import Flag, ArgStringType, FileName, StdDescriptor, FileNameOrStdDescriptor
from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameOrStdDescriptorWithIOInfo, FileNameWithIOInfo, StdDescriptorWithIOInfo, \
        add_access_to_stream_input, add_access_to_stream_output
from datatypes_new.AccessKind import AccessKind, AccessKindEnum
from annotation_generation_new.datatypes.Inputs import Inputs, InputsEnum
from util_standard import standard_repr, standard_eq


class CommandInvocationWithIOVars:

    # TODO: get_access() will not work here anymore, use access_map

    def __init__(self,
                 # types to be updated
                 cmd_name: str,
                 flag_option_list: List[Union[Flag, OptionWithIO]],
                 operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                 implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo],
                 implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo],
                 access_map
                 ) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[Union[Flag, OptionWithIO]] = flag_option_list
        self.operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]] = operand_list
        self.implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_input
        self.implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_output
        self.access_map = access_map
        # map from variables to filenames

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other: CommandInvocationWithIO):
        return standard_eq(self, other)

    @staticmethod
    def get_from_without_vars(cmd_inv_with_io: CommandInvocationWithIO, access_map):
        return CommandInvocationWithIOVars(cmd_name=cmd_inv_with_io.cmd_name,
                                    flag_option_list=cmd_inv_with_io.flag_option_list,
                                    operand_list=cmd_inv_with_io.operand_list,
                                    implicit_use_of_streaming_input=cmd_inv_with_io.implicit_use_of_streaming_input,
                                    implicit_use_of_streaming_output=cmd_inv_with_io.implicit_use_of_streaming_output,
                                    access_map=access_map)


    def substitute_inputs_and_outputs_in_cmd_invocation(self,
                                                        inputs_from: List[FileNameOrStdDescriptor],
                                                        outputs_to: List[FileNameOrStdDescriptor]) -> None:
        self.substitute_inputs_in_cmd_invocation(inputs_from)
        self.substitute_outputs_in_cmd_invocation(outputs_to)

    def substitute_inputs_in_cmd_invocation(self, inputs_from):
        remaining_inputs: List[FileNameOrStdDescriptorWithIOInfo] = [add_access_to_stream_input(input_from) for
                                                                     input_from in inputs_from]
        self.implicit_use_of_streaming_input, consumed = CommandInvocationWithIO.replace_stream_input_in_implicit_use_if_applicable(
            self.implicit_use_of_streaming_input, remaining_inputs)
        remaining_inputs = remaining_inputs[consumed:]
        self.flag_option_list, consumed = CommandInvocationWithIO.find_stream_input_in_flag_option_list_and_replace(
            self.flag_option_list, remaining_inputs)
        remaining_inputs = remaining_inputs[consumed:]
        self.operand_list, consumed = CommandInvocationWithIO.find_stream_input_in_operand_list_and_replace(
            self.operand_list, remaining_inputs)
        remaining_inputs = remaining_inputs[consumed:]
        assert len(remaining_inputs) == 0

    def substitute_outputs_in_cmd_invocation(self, outputs_to):
        remaining_outputs: List[FileNameOrStdDescriptorWithIOInfo] = [add_access_to_stream_output(output_to) for
                                                                      output_to in outputs_to]
        self.implicit_use_of_streaming_output, consumed = CommandInvocationWithIO.replace_stream_output_in_implicit_use_if_applicable(
            self.implicit_use_of_streaming_output, remaining_outputs)
        remaining_outputs = remaining_outputs[consumed:]
        self.flag_option_list, consumed = CommandInvocationWithIO.find_stream_output_in_flag_option_list_and_replace(
            self.flag_option_list, remaining_outputs)
        remaining_outputs = remaining_outputs[consumed:]
        self.operand_list, consumed = CommandInvocationWithIO.find_stream_output_in_operand_list_and_replace(
            self.operand_list, remaining_outputs)
        remaining_outputs = remaining_outputs[consumed:]
        assert len(remaining_outputs) == 0


    @staticmethod
    def find_stream_input_in_flag_option_list_and_replace(flag_option_list: List[Union[Flag, OptionWithIO]],
                                                          inputs_from: List[FileNameOrStdDescriptorWithIOInfo]) \
            -> Tuple[List[Union[Flag, OptionWithIO]], int]:
        return CommandInvocationWithIO.find_stream_something_in_flag_option_list_and_replace(flag_option_list, inputs_from, AccessKindEnum.STREAM_INPUT)

    @staticmethod
    def find_stream_output_in_flag_option_list_and_replace(flag_option_list: List[Union[Flag, OptionWithIO]],
                                                           outputs_to: List[FileNameOrStdDescriptorWithIOInfo]) \
            -> Tuple[List[Union[Flag, OptionWithIO]], int]:
        return CommandInvocationWithIO.find_stream_something_in_flag_option_list_and_replace(flag_option_list, outputs_to, AccessKindEnum.STREAM_OUTPUT)

    @staticmethod
    def find_stream_something_in_flag_option_list_and_replace(flag_option_list: List[Union[Flag, OptionWithIO]],
                                                              new_filenames_and_stddescriptors: List[FileNameOrStdDescriptorWithIOInfo],
                                                              access_to_replace: AccessKindEnum) \
            -> Tuple[List[Union[Flag, OptionWithIO]], int]:
        flag_option_list_new = []
        index_filenames_stddescriptors = 0
        for flag_option in flag_option_list:
            if isinstance(flag_option, Flag):
                flag_option_list_new.append(flag_option)
            elif isinstance(flag_option, OptionWithIO):
                if isinstance(flag_option.option_arg, FileNameWithIOInfo) or isinstance(flag_option.option_arg, StdDescriptorWithIOInfo):
                    access: AccessKind = flag_option.option_arg.get_access()
                    if access.kind == access_to_replace:
                        flag_option_list_new.append(OptionWithIO(flag_option.get_name(),
                                                                 new_filenames_and_stddescriptors[index_filenames_stddescriptors]))
                        index_filenames_stddescriptors += 1
                    else:
                        flag_option_list_new.append(flag_option)
                elif isinstance(flag_option.option_arg, ArgStringType):
                    flag_option_list_new.append(flag_option)
                else:
                    raise Exception("neither of all types for option argument")
        return (flag_option_list_new, index_filenames_stddescriptors)


    @staticmethod
    def find_stream_input_in_operand_list_and_replace(operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                                                      inputs_from: List[FileNameOrStdDescriptorWithIOInfo]) \
            -> Tuple[List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]], int]:
        return CommandInvocationWithIO.find_stream_something_in_operand_list_and_replace(operand_list, inputs_from, AccessKindEnum.STREAM_INPUT)

    @staticmethod
    def find_stream_output_in_operand_list_and_replace(operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                                                       outputs_to: List[FileNameOrStdDescriptorWithIOInfo]) \
            -> Tuple[List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]], int]:
        return CommandInvocationWithIO.find_stream_something_in_operand_list_and_replace(operand_list, outputs_to, AccessKindEnum.STREAM_INPUT)

    @staticmethod
    def find_stream_something_in_operand_list_and_replace(operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                                                          new_filenames_and_stddescriptors: List[FileNameOrStdDescriptorWithIOInfo],
                                                          access_to_replace: AccessKindEnum) \
            -> Tuple[List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]], int]:
        operand_list_new = []
        index_filenames_stddescriptors = 0
        for operand in operand_list:
            if isinstance(operand, ArgStringType):
                operand_list_new.append(operand)
            elif isinstance(operand, FileNameWithIOInfo) or isinstance(operand, StdDescriptorWithIOInfo):
                access: AccessKind = operand.get_access()
                if access.kind == access_to_replace:
                    operand_list_new.append(new_filenames_and_stddescriptors[index_filenames_stddescriptors])
                    index_filenames_stddescriptors += 1
                else:
                    operand_list_new.append(operand)
        return (operand_list_new, index_filenames_stddescriptors)


    @staticmethod
    def replace_stream_input_in_implicit_use_if_applicable(implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo],
                                                           inputs_from: List[FileNameOrStdDescriptorWithIOInfo]) \
            -> Tuple[Optional[FileNameOrStdDescriptorWithIOInfo], int]:
        if implicit_use_of_streaming_input is not None and implicit_use_of_streaming_input.access.is_stream_input():
            return (inputs_from[0], 1)
        else:
            return (implicit_use_of_streaming_input, 0)

    @staticmethod
    def replace_stream_output_in_implicit_use_if_applicable(implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo],
                                                            outputs_to: List[FileNameOrStdDescriptorWithIOInfo]) \
            -> Tuple[Optional[FileNameOrStdDescriptorWithIOInfo], int]:
        if implicit_use_of_streaming_output is not None and implicit_use_of_streaming_output.access.is_stream_output():
            return (outputs_to[0], 1)
        else:
            return (implicit_use_of_streaming_output, 0)

    def generate_inputs(self):
        # ASSUMPTION: no configuration inputs, no fallback, and option list, stdin
        streaming_inputs = []
        for operand in [self.implicit_use_of_streaming_input] + self.operand_list:
            try:
                access = self.access_map.get(operand)
                if access is not None and access.is_stream_input():
                    streaming_inputs.append(operand)
            except:
                pass
        return Inputs(InputsEnum.STREAMING, ([], streaming_inputs))

    def generate_outputs(self):
        # ASSUMPTION: only operands, no stdout
        outputs = []
        for operand in [self.implicit_use_of_streaming_output] + self.operand_list:
            try:
                access = self.access_map.get(operand)
                if access is not None and access.is_any_output():
                    outputs.append(operand)
            except:
                pass
        return outputs

    ## TODO: Q: Is there a way to abstract both mapping and traversing
    def replace_var(self, from_var, to_var):
        ## TODO: Change in all locations
        changed = False
        for i in range(len(self.operand_list)):
            operand = self.operand_list[i]
            if operand == from_var:
                self.operand_list[i] = to_var
                changed = True
                break
        if self.implicit_use_of_streaming_input == from_var:
            self.implicit_use_of_streaming_input = to_var
            changed = True
        if self.implicit_use_of_streaming_output == from_var:
            self.implicit_use_of_streaming_output = to_var
            changed = True
        if changed:
            self.access_map[to_var] = self.access_map.pop(from_var)
        assert(not from_var in self.access_map)

    # for test cases:
    def get_operands_with_config_input(self) -> List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]]:
        return [x for x in self.operand_list if
                isinstance(x, ArgStringType) or
                ((isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_config_input())]

    def get_operands_with_stream_input(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_stream_input()]

    def get_operands_with_other_input(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_other_input()]

    def get_operands_with_stream_output(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_stream_output()]

    def get_operands_with_other_output(self) -> List[FileNameOrStdDescriptorWithIOInfo]:
        return [x for x in self.operand_list if (isinstance(x, FileNameWithIOInfo) or isinstance(x, StdDescriptorWithIOInfo))
                and x.access.is_other_output()]

    def get_options_with_other_output(self) -> List[OptionWithIO]:
        only_options: List[OptionWithIO] = [x for x in self.flag_option_list if isinstance(x, OptionWithIO)]
        return [x for x in only_options if
                ((isinstance(x.option_arg, FileNameWithIOInfo) or isinstance(x.option_arg, StdDescriptorWithIOInfo)))
                and x.option_arg.access.is_other_output()]
