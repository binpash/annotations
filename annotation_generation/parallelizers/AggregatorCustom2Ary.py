from parallelizers.Aggregator_Interface import AggregatorInterface


class AggregatorCustom2Ary(AggregatorInterface):

    def __init__(self, custom_agg):
        self.custom_agg = custom_agg

    def __repr__(self):
        return f'AggCustom2Ary'

    def get_aggregator_cmd(self):
        pass
        # TODO: add information here