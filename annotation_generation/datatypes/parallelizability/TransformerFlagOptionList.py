from __future__ import annotations
from typing import Optional, List

from enum import Enum

from util import standard_repr, standard_eq
from annotation_generation.util import return_empty_list_if_none_else_itself

from datatypes.FlagOption import FlagOption


class TransformerFlagOptionListKindEnum(Enum):
    SAME_AS_SEQ = 'same_as_seq'
    ADD = 'add'
    REMOVE = 'remove'
    FILTER = 'filter'
    EMPTY = 'empty'
    # we only allow to amend arguments for options with CUSTOM
    CUSTOM = 'custom'


class TransformerFlagOptionList:

    def __init__(self,
                 kind: TransformerFlagOptionListKindEnum,
                 list_of_flags_and_options : Optional[List[FlagOption]] = None,    # None translates to empty list
                 ) -> None:
        self.kind = kind
        self.list_of_flags_and_options = return_empty_list_if_none_else_itself(list_of_flags_and_options)

    def __eq__(self, other: TransformerFlagOptionList) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    def get_flag_option_list_after_transformer_application(self, original_flag_option_list) -> List[FlagOption]:
        if self.kind == TransformerFlagOptionListKindEnum.SAME_AS_SEQ:
            return original_flag_option_list
        elif self.kind == TransformerFlagOptionListKindEnum.ADD:
            list_of_flagoptions_without_the_ones_in_original_one = [flagoption
                                                                    for flagoption in self.list_of_flags_and_options
                                                                    if flagoption not in original_flag_option_list]
            return original_flag_option_list + list_of_flagoptions_without_the_ones_in_original_one
        elif self.kind == TransformerFlagOptionListKindEnum.REMOVE:
            return [flagoption for flagoption in original_flag_option_list
                    if flagoption not in self.list_of_flags_and_options]
        elif self.kind == TransformerFlagOptionListKindEnum.FILTER:
            return [flagoption for flagoption in original_flag_option_list
                    if flagoption in self.list_of_flags_and_options]
        elif self.kind == TransformerFlagOptionListKindEnum.EMPTY:
            return []
        elif self.kind == TransformerFlagOptionListKindEnum.CUSTOM:
            return self.list_of_flags_and_options

    ## factory methods to hide the kind in API
    @staticmethod
    def make_transformer_same_as_seq() -> TransformerFlagOptionList:
        return TransformerFlagOptionList(TransformerFlagOptionListKindEnum.SAME_AS_SEQ)

    @staticmethod
    def make_transformer_add(list_to_add) -> TransformerFlagOptionList:
        return TransformerFlagOptionList(TransformerFlagOptionListKindEnum.ADD, list_to_add)

    @staticmethod
    def make_transformer_remove(list_to_remove) -> TransformerFlagOptionList:
        return TransformerFlagOptionList(TransformerFlagOptionListKindEnum.REMOVE, list_to_remove)

    @staticmethod
    def make_transformer_filter(list_to_filter) -> TransformerFlagOptionList:
        return TransformerFlagOptionList(TransformerFlagOptionListKindEnum.FILTER, list_to_filter)

    @staticmethod
    def make_transformer_custom(new_list) -> TransformerFlagOptionList:
        return TransformerFlagOptionList(TransformerFlagOptionListKindEnum.CUSTOM, new_list)

    @staticmethod
    def return_transformer_same_as_seq_if_none_else_itself(arg: Optional[TransformerFlagOptionList]) \
            -> TransformerFlagOptionList:
        if arg is None:
            return TransformerFlagOptionList.make_transformer_same_as_seq()
        else:
            return arg
