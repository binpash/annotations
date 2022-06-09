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
        return AccessKind(AccessKindEnum.CONFIG_INPUT)

    def is_config_input(self) -> bool:
        return self.kind == AccessKindEnum.CONFIG_INPUT

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

    @staticmethod
    def get_access_from_string(value: str) -> AccessKind:
        if value == "CONFIG_INPUT":
            return AccessKind.make_config_input()
        elif value == "STREAM_INPUT":
            return AccessKind.make_stream_input()
        elif value == "OTHER_INPUT":
            print("reach input")
            return AccessKind.make_other_input()
        elif value == "STREAM_OUTPUT":
            return AccessKind.make_stream_output()
        elif value == "OTHER_OUTPUT":
            print("reach output")
            return AccessKind.make_other_output()
        else:
            raise Exception("unknown option for access kind")


class AccessKindEnum(Enum):
    CONFIG_INPUT = 0
    STREAM_INPUT = 1
    # TODO: for task parallelization, both make a difference
    OTHER_INPUT = 2     # e.g. grep with exclude, and sort with --files0-from
    STREAM_OUTPUT = 3
    OTHER_OUTPUT = 4
