from __future__ import annotations
from typing import Optional, List
from util import standard_repr
from annotation_generation.util import return_empty_list_if_none_else_itself

from enum import Enum

from datatypes.FlagOption import FlagOption
from datatypes.Operand import Operand

class AdditionalInfoMapperToAggregator(Enum):
    NO_ADD_INPUT = 0

class Aggregator:

    def __init__(self,
                 # depending on kind, the aggregator function will be applied to different inputs
                 kind: AggregatorKindEnum,
                 spec_agg_cmd_name: Optional[str] = None,
                 flag_option_list : Optional[FlagOption] = None,    # None translates to empty list
                 positional_config_list : Optional[Operand] = None, # None translates to empty list
                 additional_input : AdditionalInfoMapperToAggregator = AdditionalInfoMapperToAggregator.NO_ADD_INPUT,
                 ) -> Aggregator:
        self.kind = kind
        self.additional_input = additional_input
        # only set spec_agg_* to non-None if relevant
        if kind == AggregatorKindEnum.CONCATENATE \
                or kind == AggregatorKindEnum.ADJ_LINES_MERGE:
            self.spec_agg_cmd_name: Optional[str] = None
            self.spec_agg_flag_option_list: Optional[List[FlagOption]] = None
            self.spec_agg_positional_config_list: Optional[List[Operand]] = None
        elif kind == AggregatorKindEnum.ADJ_LINES_FUNC \
            or kind == AggregatorKindEnum.CUSTOM_2_ARY \
            or kind == AggregatorKindEnum.CUSTOM_N_ARY:
            self.spec_agg_cmd_name = spec_agg_cmd_name
            self.spec_agg_flag_option_list = return_empty_list_if_none_else_itself(flag_option_list),
            self.spec_agg_positional_config_list = return_empty_list_if_none_else_itself(positional_config_list)
        else:
            raise Exception("no proper kind given for Aggregator")

    def __eq__(self, other: Aggregator) -> bool:
        return self.kind == other.kind and self.get_func() == other.get_func()

    def __repr__(self) -> str:
        return standard_repr(self)

    # def get_func(self) -> Optional[str]:
    #     if self.kind == AggregatorKindEnum.ADJ_LINES_FUNC:
    #         return self.spec_agg_cmd_name
    #     elif self.kind == AggregatorKindEnum.CUSTOM_2_ARY:
    #         return self.spec_agg_cmd_name
    #     elif self.kind == AggregatorKindEnum.CUSTOM_N_ARY:
    #         return self.spec_agg_cmd_name
    #     return None

    # TODO: add factory methods again
    # @staticmethod
    # def make_aggregator_concatenate() -> Aggregator:
    #     return Aggregator(AggregatorKindEnum.CONCATENATE)
    #
    # @staticmethod
    # def make_aggregator_adj_lines_merge() -> Aggregator:
    #     return Aggregator(AggregatorKindEnum.ADJ_LINES_MERGE)
    #
    # @staticmethod
    # def make_aggregator_adj_lines_func(func: str) -> Aggregator:
    #     return Aggregator(AggregatorKindEnum.ADJ_LINES_FUNC, func)
    #
    # @staticmethod
    # def make_aggregator_custom_2_ary(func: str) -> Aggregator:
    #     return Aggregator(AggregatorKindEnum.CUSTOM_2_ARY, func)
    #
    # @staticmethod
    # def make_aggregator_custom_n_ary(func: str) -> Aggregator:
    #     return Aggregator(AggregatorKindEnum.CUSTOM_N_ARY, func)


class AggregatorKindEnum(Enum):
    CONCATENATE = 1
    ADJ_LINES_MERGE = 2
    ADJ_LINES_FUNC = 3
    CUSTOM_2_ARY = 4
    CUSTOM_N_ARY = 5

