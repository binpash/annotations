from enum import Enum


class Splitter:

    def __init__(self, kind):
        self.kind = kind

    def __eq__(self, other):
        return self.kind == other.kind

    def __repr__(self):
        return f'{self.kind}'

    @staticmethod
    def make_splitter_indiv_files():
        return Splitter(SplitterKindEnum.INDIV_FILES)

    @staticmethod
    def make_splitter_round_robin():
        return Splitter(SplitterKindEnum.ROUND_ROBIN)

    @staticmethod
    def make_splitter_consec_junks():
        return Splitter(SplitterKindEnum.CONSEC_JUNKS)


class SplitterKindEnum(Enum):
    INDIV_FILES = 1
    ROUND_ROBIN = 2
    CONSEC_JUNKS = 3

