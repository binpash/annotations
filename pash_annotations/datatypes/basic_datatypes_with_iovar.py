from typing import Union
from pash_annotations.datatypes.basic_datatypes import ArgStringType

IOVar = int


class OptionWithIOVar:
    def __init__(self, name: str, option_arg: Union[IOVar, ArgStringType]) -> None:
        self.option_name: str = name
        self.option_arg: Union[IOVar, ArgStringType] = option_arg

    def get_name(self) -> str:
        return self.option_name

    def get_arg(self) -> Union[IOVar, ArgStringType]:
        return self.option_arg

    def get_arg_with_ioinfo(self) -> Union[IOVar, ArgStringType]:
        return self.option_arg
