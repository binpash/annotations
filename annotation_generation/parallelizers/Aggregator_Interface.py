from abc import ABC, abstractmethod


class AggregatorInterface(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_aggregator_cmd(self):
        pass
