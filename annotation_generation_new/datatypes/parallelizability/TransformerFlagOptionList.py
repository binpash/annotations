from __future__ import annotations
from typing import Optional, List
from datatypes_new.BasicDatatypes import FlagOption

from abc import ABC, abstractmethod

from util_standard import standard_repr, standard_eq
from util_new import foldl


# We offer the following different transformers for flag option lists
#     SAME_AS_SEQ   : the original flag option list
#     ADD           : the provided list (deduped) will be added to the original one
#     REMOVE        : the provided list will be removed from the original list
#     FILTER        : only entries from the provided list will be kept of the original one
#     EMPTY         : the new flag option list is empty
#     CUSTOM        : custom flag option list
#     Note that we only allow to amend arguments for options with CUSTOM


class TransformerFlagOptionList(ABC):

    def __eq__(self, other: TransformerFlagOptionList) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    @abstractmethod
    def get_flag_option_list_after_transformer_application(self, original_flag_option_list: List[FlagOption]) -> List[FlagOption]:
        pass

    @staticmethod
    def return_transformer_empty_if_none_else_itself(arg: Optional[TransformerFlagOptionList]) \
            -> TransformerFlagOptionList:
        if arg is None:
            return make_transformer_empty()
        else:
            return arg

    @staticmethod
    def return_transformer_same_as_seq_if_none_else_itself(arg: Optional[TransformerFlagOptionList]) \
            -> TransformerFlagOptionList:
        if arg is None:
            return make_transformer_same_as_seq()
        else:
            return arg

    @staticmethod
    def apply_individual_transformer(transformer: TransformerFlagOptionList,
                                     current_list: List[FlagOption]
                                     ) -> List[FlagOption]:
        return transformer.get_flag_option_list_after_transformer_application(current_list)


class TransformerFlagOptionListSeq(TransformerFlagOptionList):

    def __init__(self) -> None:
        pass

    def get_flag_option_list_after_transformer_application(self, original_flag_option_list: List[FlagOption]) -> List[FlagOption]:
        return original_flag_option_list

class TransformerFlagOptionListAdd(TransformerFlagOptionList):

    def __init__(self, list_to_add: List[FlagOption]) -> None:
        self.list_to_add: List[FlagOption] = list_to_add

    def get_flag_option_list_after_transformer_application(self, original_flag_option_list: List[FlagOption]) -> List[FlagOption]:
        list_of_flagoptions_without_the_ones_in_original_one = [flagoption
                                                                for flagoption in self.list_to_add
                                                                if flagoption not in original_flag_option_list]
        return original_flag_option_list + list_of_flagoptions_without_the_ones_in_original_one

class TransformerFlagOptionListRemove(TransformerFlagOptionList):

    def __init__(self, list_to_remove: List[FlagOption]) -> None:
        self.list_to_remove = list_to_remove

    def get_flag_option_list_after_transformer_application(self, original_flag_option_list: List[FlagOption]) -> List[FlagOption]:
        return [flagoption for flagoption in original_flag_option_list
                if flagoption not in self.list_to_remove]

class TransformerFlagOptionListFilter(TransformerFlagOptionList):

    def __init__(self, list_filter: List[FlagOption]) -> None:
        self.list_filter = list_filter

    def get_flag_option_list_after_transformer_application(self, original_flag_option_list: List[FlagOption]) -> List[FlagOption]:
        return [flagoption for flagoption in original_flag_option_list
                if flagoption in self.list_filter]

class TransformerFlagOptionListEmpty(TransformerFlagOptionList):

    def __init__(self) -> None:
        pass

    def get_flag_option_list_after_transformer_application(self, original_flag_option_list: List[FlagOption]) -> List[FlagOption]:
        return []

class TransformerFlagOptionListCustom(TransformerFlagOptionList):

    def __init__(self, list_custom: List[FlagOption]) -> None:
        self.list_custom = list_custom

    def get_flag_option_list_after_transformer_application(self, original_flag_option_list: List[FlagOption]) -> List[FlagOption]:
        return self.list_custom

## factory methods to hide details for API
def make_transformer_same_as_seq() -> TransformerFlagOptionList:
    return TransformerFlagOptionListSeq()

def make_transformer_add(list_to_add) -> TransformerFlagOptionList:
    return TransformerFlagOptionListAdd(list_to_add)

def make_transformer_remove(list_to_remove) -> TransformerFlagOptionList:
    return TransformerFlagOptionListRemove(list_to_remove)

def make_transformer_empty() -> TransformerFlagOptionList:
    return TransformerFlagOptionListEmpty()

def make_transformer_filter(list_to_filter) -> TransformerFlagOptionList:
    return TransformerFlagOptionListFilter(list_to_filter)

def make_transformer_custom(list_custom) -> TransformerFlagOptionList:
    return TransformerFlagOptionListCustom(list_custom)


# a class which allows to chain multiple Transformers
# implements the same method as the others for uniformity
class ChainTransformerFlagOptionList(TransformerFlagOptionList):

    def __init__(self, list_transformers) -> None:
        self.list_transformers = list_transformers

    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[FlagOption]
                                                           ) -> List[FlagOption]:
        return foldl(TransformerFlagOptionList.apply_individual_transformer, original_flag_option_list, self.list_transformers)

