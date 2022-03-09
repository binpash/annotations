from enum import Enum


class Aggregator:

    def __init__(self, kind, func=None):
        self.kind = kind
        match kind:
            # TODO: unify names
            case AggregatorKindEnum.ADJ_LINES_FUNC:
                self.adj_func = func
            case AggregatorKindEnum.CUSTOM_2_ARY:
                self.cus2_func = func
            case AggregatorKindEnum.CUSTOM_N_ARY:
                self.custom_aggregator = func

    def __eq__(self, other):
        return self.kind == other.kind and self.get_func() == other.get_func()

    def __repr__(self):
        return f'{self.kind} \t {self.get_func()}'

    def get_func(self):
        match self.kind:
            case AggregatorKindEnum.ADJ_LINES_FUNC:
                return self.adj_func
            case AggregatorKindEnum.CUSTOM_2_ARY:
                return self.cus2_func
            case AggregatorKindEnum.CUSTOM_N_ARY:
                return self.custom_aggregator
        return None

    @staticmethod
    def make_aggregator_concatenate():
        return Aggregator(AggregatorKindEnum.CONCATENATE)

    @staticmethod
    def make_aggregator_adj_lines_merge():
        return Aggregator(AggregatorKindEnum.ADJ_LINES_MERGE)

    @staticmethod
    def make_aggregator_adj_lines_func(func):
        return Aggregator(AggregatorKindEnum.ADJ_LINES_FUNC, func)

    @staticmethod
    def make_aggregator_custom_2_ary(func):
        return Aggregator(AggregatorKindEnum.CUSTOM_2_ARY, func)

    @staticmethod
    def make_aggregator_custom_n_ary(func):
        return Aggregator(AggregatorKindEnum.CUSTOM_n_ARY, func)


class AggregatorKindEnum(Enum):
    CONCATENATE = 1
    ADJ_LINES_MERGE = 2
    ADJ_LINES_FUNC = 3
    CUSTOM_2_ARY = 4
    CUSTOM_N_ARY = 5

