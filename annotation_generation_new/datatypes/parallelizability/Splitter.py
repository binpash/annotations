from enum import Enum


class SplitterKindEnum(Enum):
    INDIV_FILES = 1
    ROUND_ROBIN_PLAIN = 2
    ROUND_ROBIN_UNWRAP_FLAG = 3
    CONSEC_CHUNKS = 4


class Splitter:

    def __init__(self, kind: SplitterKindEnum) -> None:
        self.kind = kind

    def __eq__(self, other) -> bool:
        return self.kind == other.kind

    def __repr__(self) -> str:
        return f'{self.kind}'

    def is_splitter_round_robin(self) -> bool:
        return self.kind == SplitterKindEnum.ROUND_ROBIN_PLAIN

    def is_splitter_round_robin_with_unwrap_flag(self) -> bool:
        return self.kind == SplitterKindEnum.ROUND_ROBIN_UNWRAP_FLAG

    def is_splitter_consec_chunks(self) -> bool:
        return self.kind == SplitterKindEnum.CONSEC_CHUNKS

# currently not used
def make_splitter_indiv_files() -> Splitter:
    return Splitter(SplitterKindEnum.INDIV_FILES)

def make_splitter_round_robin() -> Splitter:
    return Splitter(SplitterKindEnum.ROUND_ROBIN_PLAIN)

def make_splitter_round_robin_with_unwrap() -> Splitter:
    return Splitter(SplitterKindEnum.ROUND_ROBIN_UNWRAP_FLAG)

def make_splitter_consec_chunks() -> Splitter:
    return Splitter(SplitterKindEnum.CONSEC_CHUNKS)

