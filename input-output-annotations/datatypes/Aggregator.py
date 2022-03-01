from enum import Enum


class Aggregator:

    def __init__(self, kind, cmd=None):
        self.kind = kind
        if self.kind is not AggregatorKindEnum.CONCATEN:
            self.command = cmd

    def __repr__(self):
        return f'{self.kind}'

    @staticmethod
    def make_aggregator_concatenation():
        return Aggregator(AggregatorKindEnum.CONCATEN)

    @staticmethod
    def make_aggregator_adjacent_lines(adj_line_aggregator):
        return Aggregator(AggregatorKindEnum.ADJ_LINE, adj_line_aggregator)

    @staticmethod
    def make_aggregator_custom_2_ary(custom_2_ary_aggregator):
        return Aggregator(AggregatorKindEnum.CUSTOM_2, custom_2_ary_aggregator)

    @staticmethod
    def make_aggregator_custom_n_ary(custom_n_ary_aggregator):
        return Aggregator(AggregatorKindEnum.CUSTOM_N, custom_n_ary_aggregator)


class AggregatorKindEnum(Enum):
    CONCATEN = 1
    ADJ_LINE = 2
    CUSTOM_2 = 3
    CUSTOM_N = 4

