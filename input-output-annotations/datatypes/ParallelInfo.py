class ParallelInfo:

    def __init__(self, splitter, mapper, aggregator):
        self.splitter = splitter
        self.mapper = mapper
        self.aggregator = aggregator

    def __repr__(self):
        return f'parallelaziblity information: \n' \
               f'splitter: {self.splitter} \n' \
               f'mapper: {self.mapper} \n' \
               f'aggregator: {self.aggregator} \n'
