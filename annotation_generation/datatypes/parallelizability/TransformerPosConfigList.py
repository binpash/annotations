from __future__ import annotations
from typing import Optional, Union, List, NewType, Any

from enum import Enum

from annotation_generation.util import return_empty_list_if_none_else_itself
from util import standard_repr, standard_eq

from datatypes.FileDescriptor import FileDescriptor

class ListIndexEnum(Enum):
    FIRST = 'first'
    LAST = 'last'

GeneralIndex = NewType('GeneralIndex', Union[int, ListIndexEnum])

def compute_actual_index(index: GeneralIndex, current_list: List[FileDescriptor]) -> int:
    actual_index = index
    if index is ListIndexEnum.FIRST:
        actual_index = 0
    elif index is ListIndexEnum.LAST:
        actual_index = len(current_list)
    return actual_index

class TransformerPosConfigListKindEnum(Enum):
    SAME_AS_SEQ = 'same_as_seq'
    ADD = 'add'         # [(GeneralIndex, arg)]
    REMOVE = 'remove'   # [GeneralIndex]
    CUSTOM = 'custom'
    # we do not offer EMPTY here since it will be error-prone,
    # would need to update certain flags not to change things in weird ways

DataTypeSEQ = NewType('DataTypeSeq', List[Any]) # actually always empty list
DataTypeAdd = NewType('DataTypeAdd', List[(GeneralIndex, FileDescriptor)])
DataTypeRemove = NewType('DataTypeRemove', List[GeneralIndex])
DataTypeCustom = NewType('DataTypeCustom', List[FileDescriptor])

class TransformerPosConfigList:

    def __init__(self,
                 kind: TransformerPosConfigListKindEnum,
                 data: Optional[Union[DataTypeAdd, DataTypeRemove, DataTypeCustom]] = None, # None does NOT translate to []
                 ) -> None:
        self.kind = kind
        self.data: Union[DataTypeSEQ, DataTypeAdd, DataTypeRemove, DataTypeCustom] = return_empty_list_if_none_else_itself(data)

    def __eq__(self, other: TransformerPosConfigList) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    def get_positional_config_list_after_transformer_application(self, original_list: List[FileDescriptor]) \
        -> List[FileDescriptor]:
        if self.kind == TransformerPosConfigListKindEnum.SAME_AS_SEQ:
            return original_list
        elif self.kind == TransformerPosConfigListKindEnum.ADD:
            updated_list = original_list
            for (index, filedescriptor) in self.data:
                actual_index = compute_actual_index(index, updated_list)
                updated_list.insert(actual_index, filedescriptor)
            return updated_list
        elif self.kind == TransformerPosConfigListKindEnum.REMOVE:
            updated_list = original_list
            for (index, filedescriptor) in self.data:
                actual_index = compute_actual_index(index, updated_list)
                updated_list.remove(actual_index)
            return updated_list
        elif self.kind == TransformerPosConfigListKindEnum.CUSTOM:
            return self.data


    ## factory methods to hide the kind in API
    @staticmethod
    def make_transformer_same_as_seq():
        return TransformerPosConfigList(TransformerPosConfigListKindEnum.SAME_AS_SEQ)

    @staticmethod
    def make_transformer_add(list_to_add):
        return TransformerPosConfigList(TransformerPosConfigListKindEnum.ADD, list_to_add)

    @staticmethod
    def make_transformer_remove(list_to_remove):
        return TransformerPosConfigList(TransformerPosConfigListKindEnum.REMOVE, list_to_remove)

    @staticmethod
    def make_transformer_custom(new_list):
        return TransformerPosConfigList(TransformerPosConfigListKindEnum.CUSTOM, new_list)

    @staticmethod
    def return_transformer_same_as_seq_if_none_else_itself(arg: Optional[TransformerPosConfigList]) \
            -> TransformerPosConfigList:
        if arg is None:
            return TransformerPosConfigList.make_transformer_same_as_seq()
        else:
            return arg

