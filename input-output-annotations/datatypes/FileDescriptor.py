from enum import Enum


class FileDescriptor:

    def __init__(self, name):
        # name should be a number
        self.name = name

    def __repr__(self):
        return str(self.name)

    def __eq__(self, other):
        return self.name == other.name

    @staticmethod
    def get_stdin_fd():
        return FileDescriptor(FileDescriptorEnum.STDIN)

    @staticmethod
    def get_stdout_fd():
        return FileDescriptor(FileDescriptorEnum.STDOUT)


class FileDescriptorEnum(Enum):
    STDIN = 0
    STDOUT = 1
    STDERR = 2
