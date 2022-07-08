from util_new import standard_eq, standard_repr
from enum import Enum


class AccessKindEnum(Enum):
    CONFIG_INPUT = 0
    STREAM_INPUT = 1
    CONTAINER_FOR_INPUT = 2     # e.g. sort with --files0-from -> does not work easily for task parallelization
    EXCLUDES_FROM_INPUT = 3     # e.g. grep with exclude -> does not affect task parallelization
    OTHER_INPUT = 4
    STREAM_OUTPUT = 5
    OTHER_OUTPUT = 6


class AccessKind:

    def __init__(self, kind) -> None:
        self.kind : AccessKindEnum = kind

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def is_config_input(self) -> bool:
        return self.kind == AccessKindEnum.CONFIG_INPUT

    def is_stream_input(self) -> bool:
        return self.kind == AccessKindEnum.STREAM_INPUT

    def is_container_for_input(self) -> bool:
        return self.kind == AccessKindEnum.CONTAINER_FOR_INPUT

    def is_excludes_from_input(self) -> bool:
        return self.kind == AccessKindEnum.EXCLUDES_FROM_INPUT

    def is_other_input(self) -> bool:
        return self.kind == AccessKindEnum.OTHER_INPUT

    def is_any_input(self):
        return self.is_config_input() or self.is_stream_input() or self.is_other_input() \
               or self.is_container_for_input() or self.is_excludes_from_input()

    def is_stream_output(self):
        return self.kind == AccessKindEnum.STREAM_OUTPUT

    def is_other_output(self):
        return self.kind == AccessKindEnum.OTHER_OUTPUT

    def is_any_output(self):
        return self.is_stream_output() or self.is_other_output()

def make_config_input() -> AccessKind:
    return AccessKind(AccessKindEnum.CONFIG_INPUT)

def make_stream_input() -> AccessKind:
    return AccessKind(AccessKindEnum.STREAM_INPUT)

def make_container_for_input() -> AccessKind:
    return AccessKind(AccessKindEnum.CONTAINER_FOR_INPUT)

def make_excludes_from_input() -> AccessKind:
    return AccessKind(AccessKindEnum.EXCLUDES_FROM_INPUT)

def make_other_input() -> AccessKind:
    return AccessKind(AccessKindEnum.OTHER_INPUT)

def make_stream_output() -> AccessKind:
    return AccessKind(AccessKindEnum.STREAM_OUTPUT)

def make_other_output() -> AccessKind:
    return AccessKind(AccessKindEnum.OTHER_OUTPUT)

def get_access_from_string(value: str) -> AccessKind:
    if value == "CONFIG_INPUT":
        return make_config_input()
    elif value == "STREAM_INPUT":
        return make_stream_input()
    elif value == "CONTAINER_FOR_INPUT":
        return make_container_for_input()
    elif value == "EXCLUDES_FROM_INPUT":
        return make_excludes_from_input()
    elif value == "OTHER_INPUT":
        return make_other_input()
    elif value == "STREAM_OUTPUT":
        return make_stream_output()
    elif value == "OTHER_OUTPUT":
        return make_other_output()
    else:
        raise Exception("unknown option for access kind")
