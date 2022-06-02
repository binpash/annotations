from __future__ import annotations
from enum import Enum

class AccessKind:

    def __init__(self, kind) -> None:
        self.kind : AccessKindEnum = kind

    @staticmethod
    def make_conf_input() -> AccessKind:
        return AccessKind(AccessKindEnum.CONF_INPUT)

    @staticmethod
    def make_stream_input() -> AccessKind:
        return AccessKind(AccessKindEnum.STREAM_INPUT)

    @staticmethod
    def make_other_input() -> AccessKind:
        return AccessKind(AccessKindEnum.OTHER_INPUT)

    @staticmethod
    def make_output() -> AccessKind:
        return AccessKind(AccessKindEnum.OUTPUT)

    def is_any_input(self):
        return self.kind == AccessKindEnum.CONF_INPUT \
                or self.kind == AccessKindEnum.STREAM_INPUT \
                or self.kind == AccessKindEnum.OTHER_INPUT

    def is_output(self):
        return self.kind == AccessKindEnum.OUTPUT


class AccessKindEnum(Enum):
    CONF_INPUT = 0
    STREAM_INPUT = 1
    OTHER_INPUT = 2
    OUTPUT = 3

