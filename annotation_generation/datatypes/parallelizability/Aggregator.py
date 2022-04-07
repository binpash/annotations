from __future__ import annotations
from typing import Optional, List
from util import standard_repr, standard_eq
from annotation_generation.util import return_empty_flag_option_list_if_none_else_itself, return_empty_pos_config_list_if_none_else_itself

from annotation_generation.datatypes.parallelizability.AggregatorKind import AggregatorKindEnum

from datatypes.FlagOption import FlagOption, OptionArgPosConfigType


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
