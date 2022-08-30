from typing import Optional, List, Union

from datatypes_new.BasicDatatypesWithIOVar import OptionWithIOVar, IOVar
from util_standard import standard_repr, standard_eq

from datatypes_new.BasicDatatypes import Flag, ArgStringType
from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameOrStdDescriptorWithIOInfo
from datatypes_new.CommandInvocationWithIOVars import CommandInvocationWithIOVars

class Mapper(CommandInvocationWithIOVars):

    # Assumption: 1 streaming input and 1 streaming output, to substitute the (new) input and output

    def __init__(self,
                 cmd_name: str,
                 flag_option_list : List[Union[Flag, OptionWithIOVar]],
                 operand_list : List[Union[ArgStringType, IOVar]],
                 implicit_use_of_streaming_input: Optional[IOVar],
                 implicit_use_of_streaming_output: Optional[IOVar],
                 access_map
                 ) -> None:
        CommandInvocationWithIOVars.__init__(self,
                                         cmd_name,
                                         flag_option_list,
                                         operand_list,
                                         implicit_use_of_streaming_input,
                                         implicit_use_of_streaming_output,
                                         access_map)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    @staticmethod
    def make_same_as_seq_mapper_from_command_invocation(command_invocation_with_io: CommandInvocationWithIOVars):
        return Mapper(command_invocation_with_io.cmd_name,
                      command_invocation_with_io.flag_option_list,
                      command_invocation_with_io.operand_list,
                      command_invocation_with_io.implicit_use_of_streaming_input,
                      command_invocation_with_io.implicit_use_of_streaming_output,
                      command_invocation_with_io.access_map)
