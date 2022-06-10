from __future__ import annotations
from typing import List, Union, Optional

from datatypes_new.BasicDatatypes import Flag, ArgStringType
from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameOrStdDescriptorWithIOInfo, FileNameWithIOInfo, StdDescriptorWithIOInfo
from util_standard import standard_repr, standard_eq

class CommandInvocationWithIO:

    def __init__(self,
                 cmd_name: str,
                 flag_option_list: List[Union[Flag, OptionWithIO]],
                 operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]],
                 implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo],
                 implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo],
                 ) -> None:
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[Union[Flag, OptionWithIO]] = flag_option_list
        self.operand_list: List[Union[ArgStringType, FileNameOrStdDescriptorWithIOInfo]] = operand_list
        self.implicit_use_of_streaming_input: Optional[FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_input
        self.implicit_use_of_streaming_output: Optional[FileNameOrStdDescriptorWithIOInfo] = implicit_use_of_streaming_output

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other: CommandInvocationWithIO):
        return standard_eq(self, other)

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
