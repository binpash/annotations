from typing import Optional, List, Union

from enum import Enum

from datatypes_new.AccessKind import make_stream_input, make_stream_output
from datatypes_new.BasicDatatypesWithIOVar import IOVar, OptionWithIOVar
from parser_new.parser import parse
from util_standard import standard_repr, standard_eq

from datatypes_new.CommandInvocationWithIOVars import CommandInvocationWithIOVars
from datatypes_new.BasicDatatypes import FileNameOrStdDescriptor, Flag
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionList, \
    return_transformer_flagoption_list_same_as_seq_if_none_else_itself, TransformerFlagOptionListCustom
# from annotation_generation_new.datatypes.parallelizability.TransformerPosConfigList import TransformerPosConfigList
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from util_new import return_default_if_none_else_itself


class MapperSpecKindEnum(Enum):
    SAME_AS_SEQ = 'same_as_seq'
    CUSTOM = 'custom'


class MapperSpec:

    def __init__(self,
                 kind: MapperSpecKindEnum = MapperSpecKindEnum.SAME_AS_SEQ,
                 spec_mapper_cmd_name: Optional[str] = None,  # None translates to original command name
                 flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,  # None translates to same as seq transformer
                 # for now, we keep everything in operand list as it is but substitute streaming input and output
                 is_implemented: bool = False
                 ) -> None:
        self.kind: MapperSpecKindEnum = kind
        self.spec_mapper_cmd_name: Optional[str] = spec_mapper_cmd_name
        self.flag_option_list_transformer: TransformerFlagOptionList = \
            return_transformer_flagoption_list_same_as_seq_if_none_else_itself(flag_option_list_transformer)
        self.is_implemented = is_implemented
        # sanity check
        if kind == MapperSpecKindEnum.SAME_AS_SEQ:
            assert spec_mapper_cmd_name is None
            assert flag_option_list_transformer is None
        elif kind == MapperSpecKindEnum.CUSTOM:
            # no assertions since None translate to "see above"
            pass
        else:
            raise Exception("unknown kind for MapperSpec")


    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    # Spec shall be hold by PaSh and once needed, gets actual mapper from this function
    # return value None if it is not yet implemented
    def get_mapper(self,
                   original_cmd_invocation: CommandInvocationWithIOVars,
                   input_from: IOVar,
                   output_to: IOVar,
                   aux_output_tos: List[IOVar]
            ) -> Optional[Mapper]:
        if not self.is_implemented:
            # this is a handle to specify future mappers without the need to implement them
            return None
        if self.kind == MapperSpecKindEnum.SAME_AS_SEQ:
            mapper = Mapper.make_same_as_seq_mapper_from_command_invocation(original_cmd_invocation)
        elif self.kind == MapperSpecKindEnum.CUSTOM:
            cmd_name = return_default_if_none_else_itself(self.spec_mapper_cmd_name, original_cmd_invocation.cmd_name)
            flag_option_list = self.flag_option_list_transformer.get_flag_option_list_after_transformer_application(
                original_cmd_invocation.flag_option_list)
            mapper = Mapper(cmd_name= cmd_name,
                            flag_option_list= flag_option_list,
                            operand_list=original_cmd_invocation.operand_list,
                            implicit_use_of_streaming_input = original_cmd_invocation.implicit_use_of_streaming_input,
                            implicit_use_of_streaming_output = original_cmd_invocation.implicit_use_of_streaming_output,
                            access_map = original_cmd_invocation.access_map)
        else:
            raise Exception("MapperSpec with unknown kind!")
        if len(aux_output_tos) == 0: # we previously checked that they are as many as specified in the parallelizer
            mapper.substitute_inputs_and_outputs_in_cmd_invocation([input_from], [output_to])
        else:
            # ASSUMPTION: operands given in that order: input, output, aux_output_1, aux_output_2, ...
            for operand in mapper.operand_list:
                assert(isinstance(operand, IOVar))
                mapper.access_map.pop(operand)
            # trick for typing...
            new_operand_list = []
            for x in [input_from, output_to] + [aux_output_to for aux_output_to in aux_output_tos]:
                new_operand_list.append(x)
            mapper.operand_list = new_operand_list
            mapper.access_map[input_from] = make_stream_input()
            mapper.access_map[output_to] = make_stream_output()
            for aux_output_to in aux_output_tos:
                mapper.access_map[aux_output_to] = make_stream_output()
            mapper.implicit_use_of_streaming_output = None
            mapper.implicit_use_of_streaming_input = None
        return mapper

## factory methods
def make_mapper_spec_seq() -> MapperSpec:
    return MapperSpec(MapperSpecKindEnum.SAME_AS_SEQ, is_implemented=True)

def return_mapper_spec_seq_if_none_else_itself(mapper_spec) -> MapperSpec:
    return return_default_if_none_else_itself(mapper_spec, make_mapper_spec_seq())

def make_mapper_spec_custom(spec_mapper_cmd_name: str,
                            flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
                            # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                            num_outputs: int = 1,
                            is_implemented: bool = False
                            ) -> MapperSpec:
    actual_flag_option_list_transformer: TransformerFlagOptionList = \
        return_transformer_flagoption_list_same_as_seq_if_none_else_itself(flag_option_list_transformer)
    # actual_pos_config_list_transformer: TransformerPosConfigList = \
    #     TransformerPosConfigList.return_transformer_same_as_seq_if_none_else_itself(pos_config_list_transformer)
    return MapperSpec(MapperSpecKindEnum.CUSTOM,
                      spec_mapper_cmd_name,
                      flag_option_list_transformer= actual_flag_option_list_transformer,
                      # pos_config_list_transformer= actual_pos_config_list_transformer,
                      is_implemented= is_implemented)

def make_mapper_spec_custom_from_string_representation(
        cmd_inv_as_str: str,
        is_implemented: bool = False) -> MapperSpec:
    cmd_inv = parse(cmd_inv_as_str)
    # currently, we assume no file names in option arguments
    # this is why we do not convert them properly but need to do this trick for typing
    # later, if option arguments contain file names, they need to get IOVar from PaSh
    new_flagoption_list: List[Union[Flag, OptionWithIOVar]] = []
    for x in cmd_inv.flag_option_list:
        assert isinstance(x, Flag)
        new_flagoption_list.append(x)
    FlagOptionListTransformer = TransformerFlagOptionListCustom(new_flagoption_list)
    return make_mapper_spec_custom(spec_mapper_cmd_name=cmd_inv.cmd_name,
                            flag_option_list_transformer=FlagOptionListTransformer,
                            is_implemented=is_implemented)
