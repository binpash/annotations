from __future__ import annotations
from typing import Optional

from enum import Enum

from util_standard import standard_repr, standard_eq

from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionList
from annotation_generation_new.datatypes.parallelizability.TransformerPosConfigList import TransformerPosConfigList
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from annotation_generation_new.datatypes.parallelizability.AdditionalInfoFromSplitter import AdditionalInfoFromSplitter
from util_new import return_default_if_none_else_itself


class MapperSpecKindEnum(Enum):
    SAME_AS_SEQ = 'same_as_seq'
    CUSTOM = 'custom'


class MapperSpec:

    def __init__(self,
                 kind: MapperSpecKindEnum = MapperSpecKindEnum.SAME_AS_SEQ,
                 spec_mapper_cmd_name: Optional[str] = None,  # None translates to original command
                 # TODO: if info_splitter_to_mapper, needs to be defined here so develop a way to use it
                 flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,  # None translates to same as seq
                 pos_config_list_transformer: Optional[TransformerPosConfigList] = None,  # None translates to empty list
                 num_outputs: int = 1,
                 add_info_from_splitter: AdditionalInfoFromSplitter = AdditionalInfoFromSplitter.NO_ADD_INPUT,
                 is_implemented: bool = False
                 ) -> None:
        self.kind: MapperSpecKindEnum = kind
        self.spec_mapper_cmd_name: Optional[str] = spec_mapper_cmd_name
        self.flag_option_list_transformer: TransformerFlagOptionList = \
            TransformerFlagOptionList.return_transformer_same_as_seq_if_none_else_itself(flag_option_list_transformer)
        self.pos_config_list_transformer: TransformerPosConfigList = \
            TransformerPosConfigList.return_transformer_same_as_seq_if_none_else_itself(pos_config_list_transformer)
        self.num_outputs : int = num_outputs
        self.add_info_from_splitter: AdditionalInfoFromSplitter = add_info_from_splitter
        self.is_implemented = is_implemented
        # sanity check
        if kind == MapperSpecKindEnum.SAME_AS_SEQ:
            assert spec_mapper_cmd_name is None
            assert flag_option_list_transformer is None
            assert pos_config_list_transformer is None
        elif kind == MapperSpecKindEnum.CUSTOM:
            # no assertions since None translate to "see above"
            pass
        else:
            raise Exception("unknown kind for MapperSpec")


    def __eq__(self, other: MapperSpec) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    # Spec shall be hold by PaSh and once needed, gets actual mapper from this function
    # return value None if it is not yet implemented
    def get_mapper(self, original_cmd_invocation_prefix: CommandInvocationPrefix) -> Optional[Mapper]:
        # this is a handle to specify future aggregators without the need to implement them
        if not self.is_implemented:
            return None
        if self.kind == MapperSpecKindEnum.SAME_AS_SEQ:
            return Mapper.make_mapper_from_command_invocation_prefix(original_cmd_invocation_prefix)
        elif self.kind == MapperSpecKindEnum.CUSTOM:
            flag_option_list = self.flag_option_list_transformer.get_flag_option_list_after_transformer_application(
                original_cmd_invocation_prefix.flag_option_list)
            pos_config_list = self.pos_config_list_transformer.get_positional_config_list_after_transformer_application(
                original_cmd_invocation_prefix.positional_config_list)
            cmd_name = return_default_if_none_else_itself(self.spec_mapper_cmd_name, original_cmd_invocation_prefix.cmd_name)
            return Mapper(cmd_name= cmd_name,
                          flag_option_list= flag_option_list,
                          positional_config_list=pos_config_list,
                          num_outputs=self.num_outputs)
        else:
            raise Exception("MapperSpec with unknown kind!")

    ## factory methods
    @staticmethod
    def make_mapper_spec_seq() -> MapperSpec:
        return MapperSpec(MapperSpecKindEnum.SAME_AS_SEQ, is_implemented=True)

    @staticmethod
    def return_mapper_spec_seq_if_none_else_itself(mapper_spec) -> MapperSpec:
        return return_default_if_none_else_itself(mapper_spec, MapperSpec.make_mapper_spec_seq())

    @staticmethod
    def make_mapper_spec_custom(spec_mapper_cmd_name: str,
                                flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                                pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                                num_outputs: int = 1,
                                add_info_from_splitter: AdditionalInfoFromSplitter = AdditionalInfoFromSplitter.NO_ADD_INPUT,
                                is_implemented: bool = False
                                ) -> MapperSpec:
        actual_flag_option_list_transformer: TransformerFlagOptionList = \
            TransformerFlagOptionList.return_transformer_same_as_seq_if_none_else_itself(flag_option_list_transformer)
        actual_pos_config_list_transformer: TransformerPosConfigList = \
            TransformerPosConfigList.return_transformer_same_as_seq_if_none_else_itself(pos_config_list_transformer)
        return MapperSpec(MapperSpecKindEnum.CUSTOM,
                          spec_mapper_cmd_name,
                          flag_option_list_transformer= actual_flag_option_list_transformer,
                          pos_config_list_transformer= actual_pos_config_list_transformer,
                          num_outputs= num_outputs,
                          add_info_from_splitter=add_info_from_splitter,
                          is_implemented= is_implemented)

