
from parallelizers.Parallelizer_Interface import ParallelizerInterface
from parallelizers.AggregatorConcatenate import AggregatorConcatenate


class ParallelizerRoundRobin(ParallelizerInterface):
    # for details on what the functions do, check comments in ParallelizerInterface

    @staticmethod
    def __name__():
        return f'RoundRobin'

    @staticmethod
    def make_parallelizer_roundrobin_mapper_seq_aggregator_concat(seq):
        return ParallelizerRoundRobin(seq, AggregatorConcatenate())
