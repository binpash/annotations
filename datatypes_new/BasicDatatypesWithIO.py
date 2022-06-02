from __future__ import annotations
from typing import Union
from BasicDatatypes import FileName, StdDescriptor, StdDescriptorEnum, Option, Operand, BaseClassForBasicDatatypes
from AccessKind import AccessKind

from abc import ABC, abstractmethod

class BaseClassForBasicDatatypesWithIOInfo(ABC):

    def __init__(self, access):
        self.access = access

    def get_access(self) -> str:
        return self.access

    @staticmethod
    @abstractmethod
    def get_from_original(original, access):
        pass
        # return DERIVED_CLASS(original.get_name(), access)


class FileNameWithIOInfo(FileName, BaseClassForBasicDatatypesWithIOInfo):

    def __init__(self, name: str, access: AccessKind) -> None:
        FileName.__init__(self, name=name)
        BaseClassForBasicDatatypesWithIOInfo.__init__(self, access=access)

    @staticmethod
    def get_from_original(original, access):
        return FileNameWithIOInfo(original.get_name(), access)


class StdDescriptorWithIOInfo(StdDescriptor, BaseClassForBasicDatatypesWithIOInfo):

    def __init__(self, name: StdDescriptorEnum, access: AccessKind) -> None:
        StdDescriptor.__init__(self, name=name)
        BaseClassForBasicDatatypesWithIOInfo.__init__(self, access=access)

    @staticmethod
    def get_from_original(original, access):
        return StdDescriptorWithIOInfo(original.get_name(), access)


FileNameOrStdDescriptorWithIOInfo = Union[FileNameWithIOInfo, StdDescriptorWithIOInfo]

# only OptionWithIOInfo if argument needs it
class OptionWithIO(BaseClassForBasicDatatypes):

    def __init__(self, name: str, option_arg: FileNameOrStdDescriptorWithIOInfo) -> None:
        self.option_name : str = name
        self.option_arg : FileNameOrStdDescriptorWithIOInfo = option_arg

    def get_name(self) -> str:
        return self.option_name

    def get_arg_with_ioinfo(self) -> FileNameOrStdDescriptorWithIOInfo:
        return self.option_arg

    @staticmethod
    def get_from_original(original: Option, access: AccessKind):
        if isinstance(original.option_arg, FileName):
            new_option_arg = FileNameWithIOInfo.get_from_original(original.option_arg, access)
        elif isinstance(original.option_arg, StdDescriptor):
            new_option_arg = StdDescriptorWithIOInfo.get_from_original(original.option_arg, access)
        else:
            raise Exception("adding access information to wrong type")
        return OptionWithIO(original.get_name(), new_option_arg)


# only OptionWithIO if argument needs it
class OperandWithIO:

    def __init__(self, name: FileNameOrStdDescriptorWithIOInfo) -> None:
        self.name = name

    def get_name(self) -> FileNameOrStdDescriptorWithIOInfo:
        return self.name

    @staticmethod
    def make_operand_a_filename_with_access(original: Operand, access: AccessKind):
        filename_with_ioinfo = FileNameWithIOInfo.get_from_original(FileName(original.get_name()), access)
        return OperandWithIO(filename_with_ioinfo)

    # TODO: how to get proper type?
    # @staticmethod
    # def make_operand_a_stddescriptor_with_access(original: Operand, access: AccessKind):
    #     filename_with_ioinfo = StdDescriptorWithIOInfo.get_from_original(StdDescriptor(original.get_name()), access)
    #     return OperandWithIOInfo(filename_with_ioinfo)
