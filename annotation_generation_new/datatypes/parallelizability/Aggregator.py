from __future__ import annotations
from typing import Optional, List
from util_standard import standard_repr, standard_eq
from util_new import return_empty_flag_option_list_if_none_else_itself, return_empty_pos_config_list_if_none_else_itself

from annotation_generation_new.datatypes.parallelizability.AggregatorKind import AggregatorKindEnum

from datatypes_new.BasicDatatypes import FlagOption, OptionArgPosConfigType


class Aggregator:

    def __init__(self,
                 # depending on kind, the aggregator function will be applied to different inputs, e.g. lines
                 kind: AggregatorKindEnum,
                 cmd_name: str,
                 flag_option_list : Optional[List[FlagOption]] = None,  # None translates to empty list
                 positional_config_list : Optional[List[OptionArgPosConfigType]] = None,  # None translates to empty list
                 ) -> None:
        self.kind = kind
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[FlagOption] = return_empty_flag_option_list_if_none_else_itself(flag_option_list)
        self.positional_config_list: List[OptionArgPosConfigType] = return_empty_pos_config_list_if_none_else_itself(positional_config_list)

    def __eq__(self, other: Aggregator) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    @classmethod
    def make_aggregator_concatenate(cls) -> Aggregator:
        return cls(AggregatorKindEnum.CONCATENATE,
                   cmd_name='cat')

    @classmethod
    def make_aggregator_adj_lines_merge(cls) -> Aggregator:
        return cls(AggregatorKindEnum.ADJ_LINES_MERGE,
                   cmd_name='adj_lines_merge')

    @classmethod
    def make_aggregator_custom_2_ary(cls,
                                     cmd_name: str,
                                     flag_option_list: List[FlagOption],
                                     positional_config_list: Optional[List[OptionArgPosConfigType]] = None,
                                     ) -> Aggregator:
        return cls(AggregatorKindEnum.CUSTOM_2_ARY,
                   cmd_name=cmd_name,
                   flag_option_list=flag_option_list,
                   positional_config_list=positional_config_list)