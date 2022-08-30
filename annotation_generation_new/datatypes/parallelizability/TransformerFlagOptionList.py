from typing import Optional, List, Union
from datatypes_new.BasicDatatypes import Flag

from abc import ABC, abstractmethod

from datatypes_new.BasicDatatypesWithIOVar import OptionWithIOVar
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

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    @abstractmethod
    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]) \
            -> List[Union[Flag, OptionWithIOVar]]:
        pass

def return_transformer_flagoption_list_empty_if_none_else_itself(arg: Optional[TransformerFlagOptionList]) \
        -> TransformerFlagOptionList:
    if arg is None:
        return make_transformer_empty()
    else:
        return arg

def return_transformer_flagoption_list_same_as_seq_if_none_else_itself(arg: Optional[TransformerFlagOptionList]) \
        -> TransformerFlagOptionList:
    if arg is None:
        return make_transformer_same_as_seq()
    else:
        return arg

def apply_individual_transformer_flagoption_list(transformer: TransformerFlagOptionList,
                                                 current_list: List[Union[Flag, OptionWithIOVar]]
                                                 ) -> List[Union[Flag, OptionWithIOVar]]:
    return transformer.get_flag_option_list_after_transformer_application(current_list)

# TODO: retrieve access info for option arguments from man-page-file

class TransformerFlagOptionListSeq(TransformerFlagOptionList):

    def __init__(self) -> None:
        pass

    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]) \
            -> List[Union[Flag, OptionWithIOVar]]:
        return original_flag_option_list

class TransformerFlagOptionListAdd(TransformerFlagOptionList):

    def __init__(self, list_to_add: List[Union[Flag, OptionWithIOVar]]) -> None:
        self.list_to_add: List[Union[Flag, OptionWithIOVar]] = list_to_add

    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]) \
            -> List[Union[Flag, OptionWithIOVar]]:
        list_of_flagoptions_without_the_ones_in_original_one = [flagoption
                                                                for flagoption in self.list_to_add
                                                                if flagoption not in original_flag_option_list]
        return original_flag_option_list + list_of_flagoptions_without_the_ones_in_original_one

class TransformerFlagOptionListRemove(TransformerFlagOptionList):

    def __init__(self, list_to_remove: List[str]) -> None:
        self.list_to_remove = list_to_remove

    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]) \
            -> List[Union[Flag, OptionWithIOVar]]:
        return [flagoption for flagoption in original_flag_option_list
                if flagoption.get_name() not in self.list_to_remove]

class TransformerFlagOptionListFilter(TransformerFlagOptionList):

    def __init__(self, list_filter: List[str]) -> None:
        self.list_filter = list_filter

    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]) \
            -> List[Union[Flag, OptionWithIOVar]]:
        return [flagoption for flagoption in original_flag_option_list
                if flagoption.get_name() in self.list_filter]

class TransformerFlagOptionListEmpty(TransformerFlagOptionList):

    def __init__(self) -> None:
        pass

    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]) \
            -> List[Union[Flag, OptionWithIOVar]]:
        return []

class TransformerFlagOptionListCustom(TransformerFlagOptionList):

    def __init__(self, list_custom: List[Union[Flag, OptionWithIOVar]]) -> None:
        self.list_custom = list_custom

    def get_flag_option_list_after_transformer_application(self,
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]) \
            -> List[Union[Flag, OptionWithIOVar]]:
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
                                                           original_flag_option_list: List[Union[Flag, OptionWithIOVar]]
                                                           ) -> List[Union[Flag, OptionWithIOVar]]:
        return foldl(apply_individual_transformer_flagoption_list, original_flag_option_list, self.list_transformers)

