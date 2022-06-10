from __future__ import annotations
from typing import Optional, List, Union

from util_standard import standard_repr, standard_eq

from datatypes_new.BasicDatatypes import Flag, ArgStringType, FileName, StdDescriptor, FileNameOrStdDescriptor
from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameWithIOInfo, StdDescriptorWithIOInfo, FileNameOrStdDescriptorWithIOInfo
from datatypes_new.AccessKind import AccessKind, AccessKindEnum
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO

class Mapper(CommandInvocationWithIO):

    def __init__(self,
                 cmd_name: str,
                 flag_option_list : List[Union[Flag, OptionWithIO]],
                 operand_list : List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                 implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo],
                 implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo]
                 ) -> None:
        CommandInvocationWithIO.__init__(self,
                                         cmd_name,
                                         flag_option_list,
                                         operand_list,
                                         implicit_use_of_streaming_input,
                                         implicit_use_of_streaming_output)

    def __eq__(self, other: Mapper) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    @staticmethod
    def make_same_as_seq_mapper_from_command_invocation(command_invocation_with_io: CommandInvocationWithIO):
        return Mapper(command_invocation_with_io.cmd_name,
                      command_invocation_with_io.flag_option_list,
                      command_invocation_with_io.operand_list,
                      command_invocation_with_io.implicit_use_of_streaming_input,
                      command_invocation_with_io.implicit_use_of_streaming_output)

    def swap_input_and_output_in_mapper(self, input_from: FileNameOrStdDescriptor, output_to: FileNameOrStdDescriptor):
        if isinstance(input_from, FileName):
            input_from_with_access: FileNameOrStdDescriptorWithIOInfo = FileNameWithIOInfo.get_from_original(input_from,
                                                                                              AccessKind.make_stream_input())
        elif isinstance(input_from, StdDescriptor):
            input_from_with_access: FileNameOrStdDescriptorWithIOInfo = StdDescriptorWithIOInfo.get_from_original(input_from,
                                                                                                        AccessKind.make_stream_input())
        else:
            raise Exception("neither FileName nor StdDescriptor")
        if isinstance(output_to, FileName):
            output_to_with_access: FileNameOrStdDescriptorWithIOInfo = FileNameWithIOInfo.get_from_original(output_to,
                                                                                             AccessKind.make_stream_output())
        elif isinstance(output_to, StdDescriptor):
            output_to_with_access: FileNameOrStdDescriptorWithIOInfo = StdDescriptorWithIOInfo.get_from_original(output_to,
                                                                                                       AccessKind.make_stream_output())
        else:
            raise Exception("neither FileName nor StdDescriptor")
        self.flag_option_list = Mapper.find_stream_input_in_flag_option_list_and_replace(
            self.flag_option_list, input_from_with_access)
        self.flag_option_list = Mapper.find_stream_output_in_flag_option_list_and_replace(self.flag_option_list,
                                                                                         input_from_with_access)
        self.operand_list = Mapper.find_stream_input_in_operand_list_and_replace(
            self.operand_list, input_from_with_access)
        self.operand_list = Mapper.find_stream_output_in_operand_list_and_replace(self.operand_list, output_to_with_access)
        self.implicit_use_of_streaming_input = Mapper.replace_stream_input_in_implicit_use_if_applicable(
            self.implicit_use_of_streaming_input, input_from_with_access)
        self.implicit_use_of_streaming_output = Mapper.replace_stream_output_in_implicit_use_if_applicable(
            self.implicit_use_of_streaming_output, output_to_with_access)

    @staticmethod
    def find_stream_input_in_flag_option_list_and_replace(flag_option_list: List[Union[Flag, OptionWithIO]],
                                                          input_from: FileNameOrStdDescriptorWithIOInfo) \
            -> List[Union[Flag, OptionWithIO]]:
        return Mapper.find_stream_something_in_flag_option_list_and_replace(flag_option_list, input_from, AccessKindEnum.STREAM_INPUT)

    @staticmethod
    def find_stream_output_in_flag_option_list_and_replace(flag_option_list, output_to) \
            -> List[Union[Flag, OptionWithIO]]:
        return Mapper.find_stream_something_in_flag_option_list_and_replace(flag_option_list, output_to, AccessKindEnum.STREAM_OUTPUT)

    @staticmethod
    def find_stream_something_in_flag_option_list_and_replace(flag_option_list: List[Union[Flag, OptionWithIO]],
                                                              new_filename_stddescriptor: FileNameOrStdDescriptorWithIOInfo,
                                                              access_to_replace: AccessKindEnum) \
            -> List[Union[Flag, OptionWithIO]]:
        flag_option_list_new = []
        for flag_option in flag_option_list:
            if isinstance(flag_option, Flag):
                flag_option_list_new.append(flag_option)
            elif isinstance(flag_option, OptionWithIO):
                if isinstance(flag_option.option_arg, FileNameWithIOInfo) or isinstance(flag_option.option_arg, StdDescriptorWithIOInfo):
                    access: AccessKind = flag_option.option_arg.get_access()
                    if access.kind == access_to_replace:
                        flag_option_list_new.append(OptionWithIO(flag_option.get_name(), new_filename_stddescriptor))
                    else:
                        flag_option_list_new.append(flag_option)
                elif isinstance(flag_option.option_arg, ArgStringType):
                    flag_option_list_new.append(flag_option)
                else:
                    raise Exception("neither of all types for option argument")
        return flag_option_list_new


    @staticmethod
    def find_stream_input_in_operand_list_and_replace(operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                                                      input_from: FileNameOrStdDescriptorWithIOInfo) \
            -> List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]]:
        return Mapper.find_stream_something_in_operand_list_and_replace(operand_list, input_from, AccessKindEnum.STREAM_INPUT)

    @staticmethod
    def find_stream_output_in_operand_list_and_replace(operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                                                       output_to: FileNameOrStdDescriptorWithIOInfo) \
            -> List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]]:
        return Mapper.find_stream_something_in_operand_list_and_replace(operand_list, output_to, AccessKindEnum.STREAM_INPUT)

    @staticmethod
    def find_stream_something_in_operand_list_and_replace(operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                                                          new_filename_stddescriptor: FileNameOrStdDescriptorWithIOInfo,
                                                          access_to_replace: AccessKindEnum) \
            -> List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]]:
        operand_list_new = []
        for operand in operand_list:
            if isinstance(operand, ArgStringType):
                operand_list_new.append(operand)
            elif isinstance(operand, FileNameWithIOInfo) or isinstance(operand, StdDescriptorWithIOInfo):
                access: AccessKind = operand.get_access()
                if access.kind == access_to_replace:
                    operand_list_new.append(new_filename_stddescriptor)
                else:
                    operand_list_new.append(operand)
        return operand_list_new


    @staticmethod
    def replace_stream_input_in_implicit_use_if_applicable(implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo],
                                                           input_from: FileNameOrStdDescriptorWithIOInfo) \
            -> Optional[FileNameOrStdDescriptorWithIOInfo]:
        if implicit_use_of_streaming_input is not None and implicit_use_of_streaming_input.access.is_stream_input():
            return input_from
        else:
            return implicit_use_of_streaming_input

    @staticmethod
    def replace_stream_output_in_implicit_use_if_applicable(implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo],
                                                            output_to: FileNameOrStdDescriptorWithIOInfo) \
            -> Optional[FileNameOrStdDescriptorWithIOInfo]:
        if implicit_use_of_streaming_output is not None and implicit_use_of_streaming_output.access.is_stream_output():
            return output_to
        else:
            return implicit_use_of_streaming_output
