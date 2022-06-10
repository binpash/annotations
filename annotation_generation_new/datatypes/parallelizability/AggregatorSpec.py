from __future__ import annotations
from typing import Optional

from util_standard import standard_repr, standard_eq

from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionList
from annotation_generation_new.datatypes.parallelizability.TransformerPosConfigList import TransformerPosConfigList
from annotation_generation_new.datatypes.parallelizability.AggregatorKind import AggregatorKindEnum
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator
from util_new import return_default_if_none_else_itself

# TODO: splitting would be better for typing, similar to Transformer for FlagOptions;
#       currently hack for ADJ_LINES_SEQ to make spec_agg_cmd non-optional
#       DEFINITELY in the future, annoying side things with transformers for the changed ones (conc, merge...)

class AggregatorSpec:

    # TODO: also convert to CommandInvocationWithIO like Mapper

    def __init__(self,
                 kind: AggregatorKindEnum,
                 spec_agg_cmd_name: str,
                 flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,  # None translates to empty list
                 pos_config_list_transformer: Optional[TransformerPosConfigList] = None,  # None translates to empty list
                 is_implemented: bool = False
                 ) -> None:
        self.kind: AggregatorKindEnum = kind
        self.spec_agg_cmd_name: str = spec_agg_cmd_name # for the rest, it should be specified
        self.flag_option_list_transformer: TransformerFlagOptionList = \
            TransformerFlagOptionList.return_transformer_empty_if_none_else_itself(flag_option_list_transformer)
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
        if not self.is_implemented:
            # this is a handle to specify future aggregators without the need to implement them
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


    @classmethod
    def make_aggregator_spec_concatenate(cls) -> AggregatorSpec:
        return cls(AggregatorKindEnum.CONCATENATE,
                   spec_agg_cmd_name='cat',
                   is_implemented=True)

    @classmethod
    def make_aggregator_spec_adj_lines_merge(cls) -> AggregatorSpec:
        return cls(AggregatorKindEnum.ADJ_LINES_MERGE,
                   spec_agg_cmd_name='adj_lines_merge',   # tr -d '\n' | sed '$a\' seems to do the job
                   # TODO: change this when implementing the procedure
                   # flag_option_list_transformer=,   # or custom if needed
                   # pos_config_list_transformer=,     # or custom if needed
                   is_implemented=False)

    @classmethod
    def make_aggregator_spec_adj_lines_seq(cls,
                                           spec_agg_cmd_name='never_used_adj_lines_seq',  # dummy
                                           flag_option_list_transformer: Optional[TransformerFlagOptionList]=None,
                                           pos_config_list_transformer: Optional[TransformerPosConfigList]=None
                                           ) -> AggregatorSpec:
        return cls(AggregatorKindEnum.ADJ_LINES_SEQ,
                   spec_agg_cmd_name=spec_agg_cmd_name,
                   flag_option_list_transformer=flag_option_list_transformer,
                   pos_config_list_transformer=pos_config_list_transformer,
                   is_implemented=False)

    @classmethod
    def make_aggregator_spec_adj_lines_func(cls,
                                            spec_agg_cmd_name: str,
                                            flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                                            pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                                            is_implemented: bool= False) -> AggregatorSpec:
        return cls(kind=AggregatorKindEnum.ADJ_LINES_FUNC,
                   spec_agg_cmd_name=spec_agg_cmd_name,
                   flag_option_list_transformer=flag_option_list_transformer,
                   pos_config_list_transformer=pos_config_list_transformer,
                   is_implemented=is_implemented)

    @classmethod
    def make_aggregator_spec_custom_2_ary(cls,
                                          spec_agg_cmd_name: str,
                                          flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                                          pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                                          is_implemented: bool= False) -> AggregatorSpec:
        return cls(kind=AggregatorKindEnum.CUSTOM_2_ARY,
                   flag_option_list_transformer=flag_option_list_transformer,
                   pos_config_list_transformer=pos_config_list_transformer,
                   spec_agg_cmd_name=spec_agg_cmd_name,
                   is_implemented=is_implemented)

    @classmethod
    def make_aggregator_spec_custom_n_ary(cls,
                                          spec_agg_cmd_name: str,
                                          flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                                          pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                                          is_implemented: bool= False) -> AggregatorSpec:
        return cls(kind=AggregatorKindEnum.CUSTOM_N_ARY,
                   flag_option_list_transformer=flag_option_list_transformer,
                   pos_config_list_transformer=pos_config_list_transformer,
                   spec_agg_cmd_name=spec_agg_cmd_name,
                   is_implemented=is_implemented)

    @staticmethod
    def return_aggregator_conc_if_none_else_itself(arg: Optional[AggregatorSpec]) -> AggregatorSpec:
        return return_default_if_none_else_itself(arg, AggregatorSpec.make_aggregator_spec_concatenate())
