from __future__ import annotations
from typing import List, Tuple, Optional, Union
from datatypes_new.BasicDatatypes import OptionArgPosConfigType

from abc import ABC, abstractmethod

from enum import Enum

from util_standard import standard_repr, standard_eq

# We offer the following different transformers for positional config_new lists:
#     SAME_AS_SEQ   : the original flag option list
#     ADD           : the provided list (deduped) will be added to the original one
#     REMOVE        : the provided list will be removed from the original list
#     CUSTOM        : custom flag option list
#     Note that we only allow to amend arguments for options with CUSTOM.
#     In contrast to transformers for flag option lists, we do not provide empty and filter
#     since their use would be error-prone.
#     The interpretation of operands may change so CUSTOM should be used for this.


class ListIndexEnum(Enum):
    FIRST = 'first'
    LAST = 'last'

GeneralIndex = Union[int, ListIndexEnum]

def compute_actual_index(index: GeneralIndex, current_list: List[OptionArgPosConfigType]) -> int:
    if index is ListIndexEnum.FIRST:
        actual_index = 0
    elif index is ListIndexEnum.LAST:
        actual_index = len(current_list)
    else:
        actual_index = index
    return actual_index


class TransformerPosConfigList(ABC):

    def __eq__(self, other: TransformerPosConfigList) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    @abstractmethod
    def get_positional_config_list_after_transformer_application(self, original_list: List[OptionArgPosConfigType]) \
        -> List[OptionArgPosConfigType]:
        pass

    @staticmethod
    def return_transformer_empty_if_none_else_itself(arg: Optional[TransformerPosConfigList]) \
            -> TransformerPosConfigList:
        if arg is None:
            return make_transformer_empty()
        else:
            return arg

    @staticmethod
    def return_transformer_same_as_seq_if_none_else_itself(arg: Optional[TransformerPosConfigList]) \
            -> TransformerPosConfigList:
        if arg is None:
            return make_transformer_same_as_seq()
        else:
            return arg

class TransformerPosConfigListSeq(TransformerPosConfigList):

    def __init__(self) -> None:
        pass

    def get_positional_config_list_after_transformer_application(self, original_list: List[OptionArgPosConfigType]) \
        -> List[OptionArgPosConfigType]:
            return original_list

class TransformerPosConfigListAdd(TransformerPosConfigList):

    def __init__(self, list_to_add: List[Tuple[GeneralIndex, OptionArgPosConfigType]]) -> None:
        self.list_to_add = list_to_add

    def get_positional_config_list_after_transformer_application(self, original_list: List[OptionArgPosConfigType]) \
        -> List[OptionArgPosConfigType]:
        updated_list = original_list
        for (index, pos_config_arg) in self.list_to_add:
            actual_index = compute_actual_index(index, updated_list)
            updated_list.insert(actual_index, pos_config_arg)
        return updated_list


class TransformerPosConfigListRemove(TransformerPosConfigList):

    def __init__(self, list_to_remove: List[GeneralIndex]) -> None:
        self.list_to_remove = list_to_remove

    def get_positional_config_list_after_transformer_application(self, original_list: List[OptionArgPosConfigType]) \
            -> List[OptionArgPosConfigType]:
        updated_list = original_list
        for index in self.list_to_remove:
            actual_index : int = compute_actual_index(index, updated_list)
            del updated_list[actual_index]
        return updated_list

class TransformerPosConfigListEmpty(TransformerPosConfigList):

    def __init__(self) -> None:
        pass

    def get_positional_config_list_after_transformer_application(self, original_list: List[OptionArgPosConfigType]) \
            -> List[OptionArgPosConfigType]:
        return []

class TransformerPosConfigListCustom(TransformerPosConfigList):

    def __init__(self, list_custom: List[OptionArgPosConfigType]) -> None:
        self.list_custom = list_custom

    def get_positional_config_list_after_transformer_application(self, original_list: List[OptionArgPosConfigType]) \
            -> List[OptionArgPosConfigType]:
        return self.list_custom

## factory methods to hide details for API
def make_transformer_same_as_seq():
    return TransformerPosConfigListSeq()

def make_transformer_add(list_to_add):
    return TransformerPosConfigListAdd(list_to_add)

def make_transformer_remove(list_to_remove):
    return TransformerPosConfigListRemove(list_to_remove)

def make_transformer_empty():
    return TransformerPosConfigListEmpty()

def make_transformer_custom(list_custom):
    return TransformerPosConfigListCustom(list_custom)
