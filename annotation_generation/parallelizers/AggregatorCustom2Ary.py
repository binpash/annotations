from parallelizers.Aggregator_Interface import AggregatorInterface


class AggregatorCustom2Ary(AggregatorInterface):

    def __init__(self, cus2_func):
        self.cus2_func = cus2_func

    def __repr__(self):
        return f'AggCustom2Ary' + \
               f'{self.cus2_func}'

    def get_aggregator_cmd(self):
        pass
        # TODO: add information here