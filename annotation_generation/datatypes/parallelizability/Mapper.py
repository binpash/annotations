from __future__ import annotations
from typing import Optional

from util import standard_repr, standard_eq
from annotation_generation.util import return_empty_list_if_none_else_itself
from enum import Enum

from datatypes.FlagOption import FlagOption
from datatypes.Operand import Operand

class AdditionalInfoSplitterToMapper(Enum):
    NO_ADD_INPUT = 0

class Mapper:

    def __init__(self,
                 cmd_name: str,
                 flag_option_list : Optional[FlagOption] = None,    # None translates to empty list
                 positional_config_list : Optional[Operand] = None, # None translates to empty list
                 additional_input : AdditionalInfoSplitterToMapper = AdditionalInfoSplitterToMapper.NO_ADD_INPUT,
                 num_output : int = 1
                 ) -> Mapper:
        # for now, we also store if the mapper is the same to handle the cases similarly
        self.cmd_name = cmd_name
        self.flag_option_list = return_empty_list_if_none_else_itself(flag_option_list),
        self.positional_config_list = return_empty_list_if_none_else_itself(positional_config_list)
        self.additional_input : AdditionalInfoSplitterToMapper = additional_input
        self.num_output : int = num_output

    def __eq__(self, other: Mapper) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    # TODO: add factory methods again
    # @staticmethod
    # def make_mapper_seq() -> Mapper:
    #     return Mapper(MapperKindEnum.SAME_AS_SEQ)
    #
    # @staticmethod
    # def make_mapper_custom(custom_cmd: str) -> Mapper:
    #     return Mapper(MapperKindEnum.CUSTOM, custom_cmd)
