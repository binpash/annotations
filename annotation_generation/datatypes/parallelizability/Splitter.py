from __future__ import annotations

from enum import Enum


class Splitter:

    def __init__(self, kind: SplitterKindEnum) -> None:
        self.kind = kind

    def __eq__(self, other: Splitter) -> bool:
        return self.kind == other.kind

    def __repr__(self) -> str:
        return f'{self.kind}'

    @staticmethod
    def make_splitter_indiv_files() -> Splitter:
        return Splitter(SplitterKindEnum.INDIV_FILES)

    @staticmethod
    def make_splitter_round_robin() -> Splitter:
        return Splitter(SplitterKindEnum.ROUND_ROBIN)

    @staticmethod
    def make_splitter_consec_chunks() -> Splitter:
        return Splitter(SplitterKindEnum.CONSEC_CHUNKS)


class SplitterKindEnum(Enum):
    INDIV_FILES = 1
    ROUND_ROBIN = 2
    CONSEC_CHUNKS = 3

