from enum import Enum


class Splitter:

    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return f'{self.kind}'

    def get_command_for_splitter(self):
        # TODO: to implement
        pass

    @staticmethod
    def make_splitter_indiv_files():
        return Splitter(SplitterKindEnum.INDIV_FILES)

    @staticmethod
    def make_splitter_round_robin():
        return Splitter(SplitterKindEnum.ROUND_ROBIN)

    @staticmethod
    def make_splitter_consective_junks():
        return Splitter(SplitterKindEnum.CONS_JUNKS)


class SplitterKindEnum(Enum):
    INDIV_FILES = 1
    ROUND_ROBIN = 2
    CONS_JUNKS = 3

