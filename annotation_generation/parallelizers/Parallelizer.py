from annotation_generation.parallelizers.Splitter import Splitter
from annotation_generation.parallelizers.Aggregator import Aggregator
from annotation_generation.util import *


class Parallelizer:

    def __init__(self, splitter, core_mapper, core_aggregator, info_splitter_mapper=None, info_mapper_aggregator=None):
        self.splitter = splitter
        self.core_mapper = core_mapper
        self.core_aggregator = core_aggregator
        self.info_splitter_mapper = info_splitter_mapper
        self.info_mapper_aggregator = info_mapper_aggregator

    def __eq__(self, other):
        return self.splitter == other.splitter \
                and self.core_mapper == other.core_mapper \
                and self.core_aggregator == other.core_aggregator \
                # and self.info_splitter_mapper == other.info_splitter_mapper \
                # and self.info_mapper_aggregator == other.info_mapper_aggregator

    def __repr__(self):
        return f'Parallizer: \n' \
               f'splitter: {self.splitter} \n' \
               f'mapper attr: {self.core_mapper} \n' \
               f'aggregator attr: {self.core_aggregator} \n'

    def get_splitter(self):
        return self.splitter

    def get_mapper(self):
        return self.core_mapper

    def get_aggregator(self):
        return self.core_aggregator

    def get_info_splitter_mapper(self):
        return self.info_splitter_mapper

    def get_info_mapper_aggregator(self):
        return self.info_mapper_aggregator

    @staticmethod
    def make_parallelizer_indiv_files(mapper=None, aggregator=None):
        aggregator = return_aggregator_conc_if_none_else_itself(aggregator)
        mapper = return_mapper_seq_if_none_else_itself(mapper)
        return Parallelizer(Splitter.make_splitter_indiv_files(), mapper, aggregator)

    @staticmethod
    def make_parallelizer_round_robin(mapper=None, aggregator=None):
        aggregator = return_aggregator_conc_if_none_else_itself(aggregator)
        mapper = return_mapper_seq_if_none_else_itself(mapper)
        return Parallelizer(Splitter.make_splitter_round_robin(), mapper, aggregator)

    @staticmethod
    def make_parallelizer_consec_junks(mapper=None, aggregator=None):
        aggregator = return_aggregator_conc_if_none_else_itself(aggregator)
        mapper = return_mapper_seq_if_none_else_itself(mapper)
        return Parallelizer(Splitter.make_splitter_consective_junks(), mapper, aggregator)