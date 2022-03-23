from __future__ import annotations
from typing import Optional

from enum import Enum


class Aggregator:

    def __init__(self, kind: AggregatorKindEnum, func: Optional[str]=None) -> None:
        self.kind = kind
        if kind == AggregatorKindEnum.CONCATENATE:
            pass
        elif kind == AggregatorKindEnum.ADJ_LINES_MERGE:
            pass
        elif kind == AggregatorKindEnum.ADJ_LINES_FUNC:
            self.func = func
        elif kind == AggregatorKindEnum.CUSTOM_2_ARY:
            self.func = func
        elif kind == AggregatorKindEnum.CUSTOM_N_ARY:
            self.func = func
        else:
            raise Exception("no proper kind given for Aggregator")
        # match kind:
        #     case AggregatorKindEnum.ADJ_LINES_FUNC:
        #         self.adj_func = func
        #     case AggregatorKindEnum.CUSTOM_2_ARY:
        #         self.cus2_func = func
        #     case AggregatorKindEnum.CUSTOM_N_ARY:
        #         self.custom_aggregator = func
        #     case _:
        #         raise Exception("no proper kind given for Aggregator")

    def __eq__(self, other: Aggregator) -> bool:
        return self.kind == other.kind and self.get_func() == other.get_func()

    def __repr__(self) -> str:
        return f'{self.kind} \t {self.get_func()}'

    def get_func(self) -> Optional[str]:
        if self.kind == AggregatorKindEnum.ADJ_LINES_FUNC:
            return self.func
        elif self.kind == AggregatorKindEnum.CUSTOM_2_ARY:
            return self.func
        elif self.kind == AggregatorKindEnum.CUSTOM_N_ARY:
            return self.func
        # match self.kind:
        #     case AggregatorKindEnum.ADJ_LINES_FUNC:
        #         return self.adj_func
        #     case AggregatorKindEnum.CUSTOM_2_ARY:
        #         return self.cus2_func
        #     case AggregatorKindEnum.CUSTOM_N_ARY:
        #         return self.custom_aggregator
        return None

    @staticmethod
    def make_aggregator_concatenate() -> Aggregator:
        return Aggregator(AggregatorKindEnum.CONCATENATE)

    @staticmethod
    def make_aggregator_adj_lines_merge() -> Aggregator:
        return Aggregator(AggregatorKindEnum.ADJ_LINES_MERGE)

    @staticmethod
    def make_aggregator_adj_lines_func(func: str) -> Aggregator:
        return Aggregator(AggregatorKindEnum.ADJ_LINES_FUNC, func)

    @staticmethod
    def make_aggregator_custom_2_ary(func: str) -> Aggregator:
        return Aggregator(AggregatorKindEnum.CUSTOM_2_ARY, func)

    @staticmethod
    def make_aggregator_custom_n_ary(func: str) -> Aggregator:
        return Aggregator(AggregatorKindEnum.CUSTOM_N_ARY, func)


class AggregatorKindEnum(Enum):
    CONCATENATE = 1
    ADJ_LINES_MERGE = 2
    ADJ_LINES_FUNC = 3
    CUSTOM_2_ARY = 4
    CUSTOM_N_ARY = 5

