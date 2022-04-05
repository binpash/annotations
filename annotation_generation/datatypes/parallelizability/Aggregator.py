from __future__ import annotations
from typing import Optional, List
from util import standard_repr
from annotation_generation.util import return_empty_list_if_none_else_itself, return_default_if_none_else_itself

from annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorKindEnum

from datatypes.FlagOption import FlagOption, OptionArgPosConfigType


class Aggregator:

    def __init__(self,
                 # depending on kind, the aggregator function will be applied to different inputs, e.g. lines
                 kind: AggregatorKindEnum,
                 cmd_name: str,
                 flag_option_list : Optional[FlagOption] = None,  # None translates to empty list
                 positional_config_list : Optional[OptionArgPosConfigType] = None,  # None translates to empty list
                 ) -> Aggregator:
        self.kind = kind
        self.cmd_name: str = cmd_name
        self.flag_option_list: List[FlagOption] = return_empty_list_if_none_else_itself(flag_option_list),
        self.positional_config_list: List[OptionArgPosConfigType] = return_empty_list_if_none_else_itself(positional_config_list)

    def __eq__(self, other: Aggregator) -> bool:
        return self.kind == other.kind and self.get_func() == other.get_func()

    def __repr__(self) -> str:
        return standard_repr(self)
