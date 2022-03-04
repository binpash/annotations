
from parallelizers.Parallelizer_Interface import ParallelizerInterface
from parallelizers.AggregatorConcatenate import AggregatorConcatenate


class ParallelizerIndivFiles(ParallelizerInterface):
    # for details on what the functions do, check comments in ParallelizerInterface

    @staticmethod
    def __name__():
        return f'IndivFiles'

    @staticmethod
    def make_parallelizer_indiv_files_mapper_seq_aggregator_concat(seq):
        return ParallelizerIndivFiles(seq, AggregatorConcatenate())
