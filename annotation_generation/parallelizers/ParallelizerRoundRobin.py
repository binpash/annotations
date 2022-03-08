
from parallelizers.Parallelizer_Interface import ParallelizerInterface
from parallelizers.AggregatorConcatenate import AggregatorConcatenate
from parallelizers.AggregatorAdjacentLinesMerge import AggregatorAdjacentLinesMerge
from parallelizers.AggregatorAdjacentLinesFunc import AggregatorAdjacentLinesFunc
from parallelizers.AggregatorCustom2Ary import AggregatorCustom2Ary


class ParallelizerRoundRobin(ParallelizerInterface):
    # for details on what the functions do, check comments in ParallelizerInterface

    @staticmethod
    def __name__():
        return f'RoundRobin'

    @staticmethod
    def make_parallelizer_mapper_seq_aggregator_conc(seq):
        return ParallelizerRoundRobin(seq, AggregatorConcatenate())

    @staticmethod
    def make_parallelizer_mapper_seq_aggregator_adjm(seq):
        return ParallelizerRoundRobin(seq, AggregatorAdjacentLinesMerge())

    @staticmethod
    def make_parallelizer_mapper_custom_aggregator_conc(custom):
        return ParallelizerRoundRobin(custom, AggregatorConcatenate())

    @staticmethod
    def make_parallelizer_mapper_custom_aggregator_adjm(custom):
        return ParallelizerRoundRobin(custom, AggregatorAdjacentLinesMerge())

    @staticmethod
    def make_parallelizer_mapper_seq_aggregator_adjf(seq, adjfunc):
        return ParallelizerRoundRobin(seq, AggregatorAdjacentLinesFunc(adjfunc))

    @staticmethod
    def make_parallelizer_mapper_custom_aggregator_adjf(custom, adjfunc):
        return ParallelizerRoundRobin(custom, AggregatorAdjacentLinesFunc(adjfunc))

    @staticmethod
    def make_parallelizer_mapper_seq_aggregator_cus2(seq, cus2func):
        return ParallelizerRoundRobin(seq, AggregatorCustom2Ary(cus2func))

    @staticmethod
    def is_parallelizer_mapper_seq_aggregator_adjm(parallelizer):
        return parallelizer.core_mapper == "seq" and isinstance(parallelizer.core_aggregator, AggregatorAdjacentLinesMerge)

    @staticmethod
    def is_parallelizer_mapper_seq_aggregator_adjf(parallelizer, adj_func):
        return parallelizer.core_mapper == "seq" and isinstance(parallelizer.core_aggregator, AggregatorAdjacentLinesFunc) \
                    and parallelizer.core_aggregator.adj_func == adj_func

    @staticmethod
    def is_parallelizer_mapper_seq_aggregator_cus2(parallelizer, cus2_func):
        return parallelizer.core_mapper == "seq" and isinstance(parallelizer.core_aggregator, AggregatorCustom2Ary) \
               and parallelizer.core_aggregator.cus2_func == cus2_func

    @staticmethod
    def is_parallelizer_mapper_seq_aggregator_conc(parallelizer):
        return parallelizer.core_mapper == "seq" and isinstance(parallelizer.core_aggregator, AggregatorConcatenate)

    @staticmethod
    def is_parallelizer_mapper_custom_aggregator_adjm(parallelizer, custom):
        return parallelizer.core_mapper == custom and isinstance(parallelizer.core_aggregator, AggregatorAdjacentLinesMerge)

    @staticmethod
    def is_parallelizer_mapper_custom_aggregator_conc(parallelizer, custom):
        return parallelizer.core_mapper == custom and isinstance(parallelizer.core_aggregator, AggregatorConcatenate)
