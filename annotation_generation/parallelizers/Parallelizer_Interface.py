from abc import ABC, abstractmethod
from parallelizers.AggregatorConcatenate import AggregatorConcatenate


class ParallelizerInterface(ABC):

    def __init__(self, core_mapper, core_aggregator):
        self.core_mapper = core_mapper
        self.core_aggregator = core_aggregator

    @staticmethod
    @abstractmethod
    def __name__():
        pass

    def __eq__(self, other):
        self.__class__.__name__ = other.__class__.__name__
        self.core_mapper = other.core_mapper
        self.core_aggregator = other.core_aggregator
        pass

    def __repr__(self):
        return f'Parallizer: \n' \
               f'splitter: {self.__class__.__name__} \n' \
               f'mapper attr: {self.core_mapper} \n' \
               f'aggregator attr: {self.core_aggregator} \n'

    def get_mapper(self):
        return self.core_mapper

    def get_aggregator(self):
        return self.core_aggregator
