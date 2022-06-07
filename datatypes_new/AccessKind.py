from __future__ import annotations
from util_new import standard_eq, standard_repr
from enum import Enum

class AccessKind:

    def __init__(self, kind) -> None:
        self.kind : AccessKindEnum = kind

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    @staticmethod
    def make_config_input() -> AccessKind:
        return AccessKind(AccessKindEnum.CONF_INPUT)

    def is_config_input(self) -> bool:
        return self.kind == AccessKindEnum.CONF_INPUT

    @staticmethod
    def make_stream_input() -> AccessKind:
        return AccessKind(AccessKindEnum.STREAM_INPUT)

    def is_stream_input(self) -> bool:
        return self.kind == AccessKindEnum.STREAM_INPUT

    @staticmethod
    def make_other_input() -> AccessKind:
        return AccessKind(AccessKindEnum.OTHER_INPUT)

    def is_other_input(self) -> bool:
        return self.kind == AccessKindEnum.OTHER_INPUT

    def is_any_input(self):
        return self.is_config_input() or self.is_stream_input() or self.is_other_input()

    @staticmethod
    def make_stream_output() -> AccessKind:
        return AccessKind(AccessKindEnum.STREAM_OUTPUT)

    def is_stream_output(self):
        return self.kind == AccessKindEnum.STREAM_OUTPUT

    @staticmethod
    def make_other_output() -> AccessKind:
        return AccessKind(AccessKindEnum.OTHER_OUTPUT)

    def is_other_output(self):
        return self.kind == AccessKindEnum.OTHER_OUTPUT

    def is_any_output(self):
        return self.is_stream_output() or self.is_other_output()


class AccessKindEnum(Enum):
    CONF_INPUT = 0
    STREAM_INPUT = 1
    OTHER_INPUT = 2
    STREAM_OUTPUT = 3
    OTHER_OUTPUT = 4
