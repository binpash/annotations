from typing import Union
from datatypes_new.BasicDatatypes import FileName, StdDescriptor, StdDescriptorEnum, Operand, \
    BaseClassForBasicDatatypes, ArgStringType, get_stdout_fd, get_stdin_fd
from datatypes_new.AccessKind import AccessKind, make_stream_output, make_stream_input

from abc import ABC, abstractmethod

class BaseClassForBasicDatatypesWithIOInfo(ABC):

    def __init__(self, access: AccessKind):
        self.access = access

    def get_access(self) -> AccessKind:
        return self.access

    # @staticmethod
    # @abstractmethod
    # def get_from_original(original, access):
    #     pass
    #     # return DERIVED_CLASS(original.get_name(), access)


class FileNameWithIOInfo(FileName, BaseClassForBasicDatatypesWithIOInfo):

    def __init__(self, name: str, access: AccessKind) -> None:
        FileName.__init__(self, name=name)
        BaseClassForBasicDatatypesWithIOInfo.__init__(self, access=access)

def get_from_original_filename_with_ioinfo(original: FileName, access: AccessKind) -> FileNameWithIOInfo:
    return FileNameWithIOInfo(original.get_name(), access)


class StdDescriptorWithIOInfo(StdDescriptor, BaseClassForBasicDatatypesWithIOInfo):

    def __init__(self, name: StdDescriptorEnum, access: AccessKind) -> None:
        StdDescriptor.__init__(self, name=name)
        BaseClassForBasicDatatypesWithIOInfo.__init__(self, access=access)

def get_from_original_stddescriptor_with_ioinfo(original: StdDescriptor, access: AccessKind) -> StdDescriptorWithIOInfo:
    return StdDescriptorWithIOInfo(original.name, access)

def make_stdin_with_access_stream_input() -> StdDescriptorWithIOInfo:
    return get_from_original_stddescriptor_with_ioinfo(get_stdin_fd(), make_stream_input())

def make_stdout_with_access_output() -> StdDescriptorWithIOInfo:
    return get_from_original_stddescriptor_with_ioinfo(get_stdout_fd(), make_stream_output())

FileNameOrStdDescriptorWithIOInfo = Union[FileNameWithIOInfo, StdDescriptorWithIOInfo]

def add_access_to_stream_output(output_to):
    if isinstance(output_to, FileName):
        assert(False)
        output_to_with_access: FileNameOrStdDescriptorWithIOInfo = FileNameWithIOInfo.get_from_original_filename_with_ioinfo(output_to,
                                                                                                                             make_stream_output())
    elif isinstance(output_to, StdDescriptor):
        assert(False)
        output_to_with_access: FileNameOrStdDescriptorWithIOInfo = StdDescriptorWithIOInfo.get_from_original_stddescriptor_with_ioinfo(
            output_to,
            make_stream_output())
    else:
        raise Exception("neither FileName nor StdDescriptor")
    return output_to_with_access

def add_access_to_stream_input(input_from):
    if isinstance(input_from, FileName):
        assert(False)
        input_from_with_access: FileNameOrStdDescriptorWithIOInfo = FileNameWithIOInfo.get_from_original_filename_with_ioinfo(input_from,
                                                                                                                              make_stream_input())
    elif isinstance(input_from, StdDescriptor):
        assert(False)
        input_from_with_access: FileNameOrStdDescriptorWithIOInfo = StdDescriptorWithIOInfo.get_from_original_stddescriptor_with_ioinfo(
            input_from,
            make_stream_input())
    else:
        raise Exception("neither FileName nor StdDescriptor")
    return input_from_with_access


# only OptionWithIOInfo if argument needs it
class OptionWithIO(BaseClassForBasicDatatypes):

    def __init__(self, name: str, option_arg: Union[FileNameOrStdDescriptorWithIOInfo, ArgStringType]) -> None:
        self.option_name : str = name
        self.option_arg : Union[FileNameOrStdDescriptorWithIOInfo, ArgStringType] = option_arg

    def get_name(self) -> str:
        return self.option_name

    def get_arg(self) -> Union[FileNameOrStdDescriptorWithIOInfo, ArgStringType]:
        return self.option_arg

    def get_arg_with_ioinfo(self) -> Union[FileNameOrStdDescriptorWithIOInfo, ArgStringType]:
        return self.option_arg

    # @staticmethod
    # wrong with new types for original Option
    # def get_from_original(original: Option, access: AccessKind):
    #     if isinstance(original.option_arg, FileName):
    #         new_option_arg = FileNameWithIOInfo.get_from_original(original.option_arg, access)
    #     elif isinstance(original.option_arg, StdDescriptor):
    #         new_option_arg = StdDescriptorWithIOInfo.get_from_original(original.option_arg, access)
    #     else:
    #         raise Exception("adding access information to wrong type")
    #     return OptionWithIO(original.get_name(), new_option_arg)


# only OptionWithIO if argument needs it
class OperandWithIO:

    def __init__(self, name: FileNameOrStdDescriptorWithIOInfo) -> None:
        self.name = name

    def get_name(self) -> FileNameOrStdDescriptorWithIOInfo:
        return self.name

    @staticmethod
    def make_operand_a_filename_with_access(original: Operand, access: AccessKind):
        filename_with_ioinfo = get_from_original_filename_with_ioinfo(FileName(original.get_name()), access)
        return OperandWithIO(filename_with_ioinfo)

    # TODO: how to get proper type?
    # @staticmethod
    # def make_operand_a_stddescriptor_with_access(original: Operand, access: AccessKind):
    #     filename_with_ioinfo = StdDescriptorWithIOInfo.get_from_original(StdDescriptor(original.get_name()), access)
    #     return OperandWithIOInfo(filename_with_ioinfo)
