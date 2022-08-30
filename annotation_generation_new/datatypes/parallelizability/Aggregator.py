from typing import Optional, List, Union

from datatypes_new.BasicDatatypesWithIO import OptionWithIO, FileNameOrStdDescriptorWithIOInfo
from datatypes_new.BasicDatatypesWithIOVar import IOVar, OptionWithIOVar
from datatypes_new.CommandInvocationWithIOVars import CommandInvocationWithIOVars
from util_standard import standard_repr, standard_eq
from util_new import return_empty_flag_option_list_if_none_else_itself, return_empty_pos_config_list_if_none_else_itself

from annotation_generation_new.datatypes.parallelizability.AggregatorKind import AggregatorKindEnum

from datatypes_new.BasicDatatypes import FlagOption, OptionArgPosConfigType, Flag, ArgStringType


class Aggregator(CommandInvocationWithIOVars):

    def __init__(self,
                 # depending on kind, the aggregator function will be applied to different inputs, e.g. lines
                 kind: AggregatorKindEnum,
                 cmd_name: str,
                 flag_option_list: List[Union[Flag, OptionWithIOVar]],
                 operand_list: List[Union[ArgStringType, IOVar]],
                 implicit_use_of_streaming_input: Optional[IOVar],
                 implicit_use_of_streaming_output: Optional[IOVar],
                 access_map
                 ) -> None:
        self.kind = kind
        CommandInvocationWithIOVars.__init__(self, cmd_name, flag_option_list, operand_list, implicit_use_of_streaming_input, implicit_use_of_streaming_output, access_map)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    def is_aggregator_concatenate(self):
        return self.kind == AggregatorKindEnum.CONCATENATE

    @classmethod
    def make_aggregator_from_cmd_inv_with_io(cls, cmd_inv: CommandInvocationWithIOVars, kind: AggregatorKindEnum):
        return cls(kind, cmd_inv.cmd_name, cmd_inv.flag_option_list, cmd_inv.operand_list,
            cmd_inv.implicit_use_of_streaming_input, cmd_inv.implicit_use_of_streaming_output, cmd_inv.access_map)

    # @classmethod
    # def make_aggregator_concatenate(cls) -> Aggregator:
    #     return cls(AggregatorKindEnum.CONCATENATE,
    #                cmd_name='cat')
    #
    # @classmethod
    # def make_aggregator_adj_lines_merge(cls) -> Aggregator:
    #     return cls(AggregatorKindEnum.ADJ_LINES_MERGE,
    #                cmd_name='adj_lines_merge')
    #
    # @classmethod
    # def make_aggregator_custom_2_ary(cls,
    #                                  cmd_name: str,
    #                                  flag_option_list: List[FlagOption],
    #                                  positional_config_list: Optional[List[OptionArgPosConfigType]] = None,
    #                                  ) -> Aggregator:
    #     return cls(AggregatorKindEnum.CUSTOM_2_ARY,
    #                cmd_name=cmd_name,
    #                flag_option_list=flag_option_list,
    #                positional_config_list=positional_config_list)
