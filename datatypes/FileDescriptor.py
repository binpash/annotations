from __future__ import annotations
from typing import NewType, Union
from enum import Enum

class FileName:

    def __init__(self, name: str) -> None:
        # name should be a string
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other: FileName) -> bool:
        return self.name == other.name

class StdDescriptor:

    def __init__(self, name: StdDescriptorEnum) -> None:
        # name should be a number
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other: StdDescriptor) -> bool:
        return self.name == other.name

    @staticmethod
    def get_stdin_fd() -> StdDescriptor:
        return StdDescriptor(StdDescriptorEnum.STDIN)

    @staticmethod
    def get_stdout_fd() -> StdDescriptor:
        return StdDescriptor(StdDescriptorEnum.STDOUT)

    @staticmethod
    def get_stderr_fd() -> StdDescriptor:
        return StdDescriptor(StdDescriptorEnum.STDERR)

class StdDescriptorEnum(Enum):
    STDIN = 0
    STDOUT = 1
    STDERR = 2

# FileDescriptor = NewType('FileDescriptor', Union[FileName, StdDescriptor])
FileDescriptor = FileName | StdDescriptor
