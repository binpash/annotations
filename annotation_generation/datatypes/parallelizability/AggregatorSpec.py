from __future__ import annotations
from typing import Optional

from enum import Enum

from util import standard_repr, standard_eq

from datatypes.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionList
from annotation_generation.datatypes.parallelizability.TransformerPosConfigList import TransformerPosConfigList
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator
from annotation_generation.util import return_default_if_none_else_itself


class AggregatorKindEnum(Enum):
    CONCATENATE = 1
    ADJ_LINES_MERGE = 2
    ADJ_LINES_SEQ = 3
    ADJ_LINES_FUNC = 4
    CUSTOM_2_ARY = 5
    CUSTOM_N_ARY = 6


class AggregatorSpec:

    def __init__(self,
                 kind: AggregatorKindEnum = AggregatorKindEnum.CONCATENATE,
                 spec_agg_cmd_name: Optional[str] = None,
                 # TODO: if info_mapper_to_aggregator, needs to be defined here so develop a way to use it
                 flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,  # None translates to same as seq
                 pos_config_list_transformer: Optional[TransformerPosConfigList] = None,  # None translates to empty list
                 is_implemented: bool = False
                 ) -> None:
        self.kind: AggregatorKindEnum = kind
        if self.kind == AggregatorKindEnum.CONCATENATE:
            spec_agg_cmd_name = 'cat'
        elif self.kind == AggregatorKindEnum.ADJ_LINES_MERGE:
            spec_agg_cmd_name = 'impl_todo_merge_adj_lines' # will never be generated currently
        self.spec_agg_cmd_name: str = spec_agg_cmd_name # for the rest, it should be specified
        self.flag_option_list_transformer: TransformerFlagOptionList = \
            TransformerFlagOptionList.return_transformer_same_as_seq_if_none_else_itself(flag_option_list_transformer),
        self.pos_config_list_transformer: TransformerPosConfigList = \
            TransformerPosConfigList.return_transformer_same_as_seq_if_none_else_itself(pos_config_list_transformer)
        self.is_implemented = is_implemented

    def __eq__(self, other: AggregatorSpec) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    # Spec shall be hold by PaSh and once needed, gets actual mapper from this function
    # return value None if it is not yet implemented
    def get_aggregator(self, original_cmd_invocation_prefix: CommandInvocationPrefix) -> Optional[Aggregator]:
        # this is a handle to specify future aggregators without the need to implement them
        if not self.is_implemented:
            return None
        if self.kind == AggregatorKindEnum.ADJ_LINES_SEQ:
            self.spec_agg_cmd_name = original_cmd_invocation_prefix.cmd_name
        flag_option_list = self.flag_option_list_transformer.get_flag_option_list_after_transformer_application(
            original_cmd_invocation_prefix.flag_option_list)
        pos_config_list = self.pos_config_list_transformer.get_positional_config_list_after_transformer_application(
            original_cmd_invocation_prefix.positional_config_list)
        return Aggregator(kind=self.kind,
                          cmd_name=self.spec_agg_cmd_name, # ensured not to be None in constructor and above for SEQ
                          flag_option_list=flag_option_list,
                          positional_config_list=pos_config_list )


    @staticmethod
    def make_aggregator_concatenate(flag_option_list_transformer: Optional[TransformerFlagOptionList]=None,
                                    pos_config_list_transformer: Optional[TransformerPosConfigList]=None
                                    ) -> AggregatorSpec:
        return AggregatorSpec(AggregatorKindEnum.CONCATENATE,
                              flag_option_list_transformer=flag_option_list_transformer,
                              pos_config_list_transformer=pos_config_list_transformer,
                              is_implemented=True)

    @staticmethod
    def make_aggregator_adj_lines_merge(flag_option_list_transformer: Optional[TransformerFlagOptionList]=None,
                                        pos_config_list_transformer: Optional[TransformerPosConfigList]=None
                                        ) -> AggregatorSpec:
        return AggregatorSpec(AggregatorKindEnum.ADJ_LINES_MERGE,
                              flag_option_list_transformer=flag_option_list_transformer,
                              pos_config_list_transformer=pos_config_list_transformer,
                              is_implemented=False)

    @staticmethod
    def make_aggregator_adj_lines_seq(flag_option_list_transformer: Optional[TransformerFlagOptionList]=None,
                                        pos_config_list_transformer: Optional[TransformerPosConfigList]=None
                                        ) -> AggregatorSpec:
        return AggregatorSpec(AggregatorKindEnum.ADJ_LINES_SEQ,
                              flag_option_list_transformer=flag_option_list_transformer,
                              pos_config_list_transformer=pos_config_list_transformer,
                              is_implemented=False)

    @staticmethod
    def make_aggregator_adj_lines_func(spec_agg_cmd_name: str,
                                       flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                                       pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                                       is_implemented: bool= False) -> AggregatorSpec:
        return AggregatorSpec(kind=AggregatorKindEnum.ADJ_LINES_FUNC,
                              spec_agg_cmd_name=spec_agg_cmd_name,
                              flag_option_list_transformer=flag_option_list_transformer,
                              pos_config_list_transformer=pos_config_list_transformer,
                              is_implemented=is_implemented)

    @staticmethod
    def make_aggregator_custom_2_ary(spec_agg_cmd_name: str,
                                     flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                                     pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                                     is_implemented: bool= False) -> AggregatorSpec:
        return AggregatorSpec(kind=AggregatorKindEnum.CUSTOM_2_ARY,
                              flag_option_list_transformer=flag_option_list_transformer,
                              pos_config_list_transformer=pos_config_list_transformer,
                              spec_agg_cmd_name=spec_agg_cmd_name,
                              is_implemented=is_implemented)

    @staticmethod
    def make_aggregator_custom_n_ary(spec_agg_cmd_name: str,
                                     flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                                     pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                                     is_implemented: bool= False) -> AggregatorSpec:
        return AggregatorSpec(kind=AggregatorKindEnum.CUSTOM_N_ARY,
                              flag_option_list_transformer=flag_option_list_transformer,
                              pos_config_list_transformer=pos_config_list_transformer,
                              spec_agg_cmd_name=spec_agg_cmd_name,
                              is_implemented=is_implemented)

    @staticmethod
    def return_aggregator_conc_if_none_else_itself(arg: Optional[AggregatorSpec]) -> AggregatorSpec:
        return return_default_if_none_else_itself(arg, AggregatorSpec.make_aggregator_concatenate())
