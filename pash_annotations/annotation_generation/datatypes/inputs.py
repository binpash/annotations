from enum import Enum


class InputsEnum(Enum):
    DEFAULT = 0
    STREAMING = 1


class Inputs:

    def __init__(self, kind: InputsEnum, values):
        self.kind = kind
        self.values = values

    def is_streaming(self):
        return self.kind == InputsEnum.STREAMING

    def get_config_inputs(self):
        assert self.is_streaming()
        return self.values[0]

    def get_streaming_inputs(self):
        assert self.is_streaming()
        return self.values[1]

    def get_all_inputs(self):
        if self.kind == InputsEnum.STREAMING:
            conf_inputs = self.values[0]
            streaming_inputs = self.values[1]
            return conf_inputs + streaming_inputs
        else:
            assert(False)