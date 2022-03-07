
from parallelizers.Parallelizer_Interface import ParallelizerInterface
from parallelizers.AggregatorConcatenate import AggregatorConcatenate
from parallelizers.AggregatorAdjacentLinesFunc import AggregatorAdjacentLinesFunc


class ParallelizerIndivFiles(ParallelizerInterface):
    # for details on what the functions do, check comments in ParallelizerInterface

    @staticmethod
    def __name__():
        return f'IndivFiles'

    @staticmethod
    def make_parallelizer_mapper_seq_aggregator_conc(seq):
        return ParallelizerIndivFiles(seq, AggregatorConcatenate())

    @staticmethod
    def make_parallelizer_mapper_custom_aggregator_conc(custom):
        return ParallelizerIndivFiles(custom, AggregatorConcatenate())

    @staticmethod
    def make_parallelizer_mapper_seq_aggregator_adjf(seq, adjfunc):
        return ParallelizerIndivFiles(seq, AggregatorAdjacentLinesFunc(adjfunc))

    @staticmethod
    def is_parallelizer_mapper_seq_aggregator_conc(parallelizer):
        return parallelizer.core_mapper == "seq" and isinstance(parallelizer.core_aggregator, AggregatorConcatenate)

    @staticmethod
    def is_parallelizer_mapper_custom_aggregator_conc(parallelizer, custom):
        return parallelizer.core_mapper == custom and isinstance(parallelizer.core_aggregator, AggregatorConcatenate)

    @staticmethod
    def is_parallelizer_mapper_seq_aggregator_adjf(parallelizer, adj_func):
        return parallelizer.core_mapper == "seq" and isinstance(parallelizer.core_aggregator, AggregatorAdjacentLinesFunc) \
               and parallelizer.core_aggregator.adj_func == adj_func
