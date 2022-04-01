from __future__ import annotations

from enum import Enum


class FileDescriptor:

    def __init__(self, name: FileDescriptorEnum) -> None:
        # name should be a number
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other: FileDescriptor) -> bool:
        return self.name == other.name

    @staticmethod
    def get_stdin_fd() -> FileDescriptor:
        return FileDescriptor(FileDescriptorEnum.STDIN)

    @staticmethod
    def get_stdout_fd() -> FileDescriptor:
        return FileDescriptor(FileDescriptorEnum.STDOUT)

    @staticmethod
    def get_stderr_fd() -> FileDescriptor:
        return FileDescriptor(FileDescriptorEnum.STDERR)


class FileDescriptorEnum(Enum):
    STDIN = 0
    STDOUT = 1
    STDERR = 2
