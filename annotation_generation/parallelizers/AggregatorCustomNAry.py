from parallelizers.Aggregator_Interface import AggregatorInterface


class AggregatorCustomNAry(AggregatorInterface):

    def __init__(self, custom_agg):
        self.custom_agg = custom_agg

    def __repr__(self):
        return f'AggCustomNAry'

    def get_aggregator_cmd(self):
        pass
        # TODO: add information here