from parallelizers.Aggregator_Interface import AggregatorInterface


class AggregatorAdjacentLinesFunc(AggregatorInterface):

    def __init__(self, adj_func):
        self.adj_func = adj_func
        pass

    def __repr__(self):
        return f'AggAdjLinesFunc'

    def get_aggregator_cmd(self):
        return self.adj_func