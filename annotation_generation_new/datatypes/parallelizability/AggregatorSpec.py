from copy import deepcopy
from typing import Optional, List, Literal, Union

from abc import ABC, abstractmethod

from datatypes_new.BasicDatatypesWithIOVar import IOVar, OptionWithIOVar
from parser_new.parser import parse
from util_standard import standard_repr, standard_eq

from datatypes_new.CommandInvocationWithIOVars import CommandInvocationWithIOVars
from datatypes_new.BasicDatatypes import FileNameOrStdDescriptor, ArgStringType, Flag
from datatypes_new.AccessKind import AccessKind, make_stream_input, make_stream_output
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import TransformerFlagOptionList, \
    return_transformer_flagoption_list_same_as_seq_if_none_else_itself, TransformerFlagOptionListCustom
# from annotation_generation_new.datatypes.parallelizability.TransformerPosConfigList import TransformerPosConfigList
from annotation_generation_new.datatypes.parallelizability.AggregatorKind import AggregatorKindEnum
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator
from util_new import return_default_if_none_else_itself

# What spec needs to contain for which one:

# CONCATENATE:      only kind
# ADJ_LINES_MERGE:  only kind
# ADJ_LINES_SEQ:    only kind, return can be computed from parameters

# ADJ_LINES_FUNC:   function for adjacent lines (2 inputs)
# CUSTOM_2_ARY:     function for two blocks     (2 inputs)
# could be given as transformation of original command or parsed from string representation

# CUSTOM_N_ARY:     function for all blocks     (multiple inputs)
# as for 2 inputs but some way to specify additional inputs,
# hard-coded appended to operand list? currently no use case anyway...

class AggregatorSpec(ABC):

    def __init__(self,
                 kind: AggregatorKindEnum,
                 # spec_agg_cmd_name: str,
                 # for now, we keep everything in operand list as it is but substitute streaming input and output
                 is_implemented: bool = False
                 ) -> None:
        self.kind: AggregatorKindEnum = kind
        # self.spec_agg_cmd_name: str = spec_agg_cmd_name # for the rest, it should be specified
        # self.flag_option_list_transformer: TransformerFlagOptionList = \
        #     TransformerFlagOptionList.return_transformer_empty_if_none_else_itself(flag_option_list_transformer)
        self.is_implemented = is_implemented


    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return standard_repr(self)

    def is_aggregator_spec_concatenate(self):
        return self.kind == AggregatorKindEnum.CONCATENATE

    def is_aggregator_spec_adj_lines_merge(self):
        return self.kind == AggregatorKindEnum.ADJ_LINES_MERGE

    def is_aggregator_spec_adj_lines_seq(self):
        return self.kind == AggregatorKindEnum.ADJ_LINES_SEQ

    def is_aggregator_spec_adj_lines_func(self):
        return self.kind == AggregatorKindEnum.ADJ_LINES_FUNC

    def is_aggregator_spec_custom_2_ary(self):
        return self.kind == AggregatorKindEnum.CUSTOM_2_ARY

    def is_aggregator_spec_custom_n_ary(self):
        return self.kind == AggregatorKindEnum.CUSTOM_N_ARY

    # Spec shall be hold by PaSh and once needed, gets actual aggregator from this function
    # return value None if it is not yet implemented
    # PaSh ought to provide the correct input based on the kind of aggregator, e.g., line
    # for CONCATENATE and CUSTOM_N_ARY, we need to provide the number of inputs to give back
    @abstractmethod
    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIOVars,
                       inputs_from: List[Union[IOVar, ArgStringType]],
                       # ArgStringType needed for typing, only IOVar provided
                       output_to: IOVar
                       ) -> Optional[Aggregator]:
        pass

    @abstractmethod
    def get_actual_2_ary_aggregator_with_aux(self,
                                             fst_normal_input: FileNameOrStdDescriptor,
                                             fst_aux_inputs_from: List[FileNameOrStdDescriptor],
                                             snd_normal_input: FileNameOrStdDescriptor,
                                             snd_aux_inputs_from: List[FileNameOrStdDescriptor],
                                             output_to: FileNameOrStdDescriptor,
                                             aux_outputs_to: List[FileNameOrStdDescriptor]
                                             ):
        pass

    def get_kind(self):
        return self.kind

def make_aggregator_spec_concatenate() -> AggregatorSpec:
    return AggregatorSpecNonFunc(AggregatorKindEnum.CONCATENATE, is_implemented=True)

def make_aggregator_spec_adj_lines_merge() -> AggregatorSpec:
    return AggregatorSpecNonFunc(AggregatorKindEnum.ADJ_LINES_MERGE, is_implemented=False)

def make_aggregator_spec_adj_lines_seq() -> AggregatorSpec:
    return AggregatorSpecNonFunc(AggregatorKindEnum.ADJ_LINES_SEQ, is_implemented=False)

def make_aggregator_spec_adj_lines_func_from_cmd_inv_with_transformers(
        flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
        # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
        is_implemented: bool = False) -> AggregatorSpec:
    return AggregatorSpecFuncTransformer(kind=AggregatorKindEnum.ADJ_LINES_FUNC,
                                         flag_option_list_transformer=flag_option_list_transformer,
                                         # pos_config_list_transformer=pos_config_list_transformer,
                                         is_implemented=is_implemented)

def make_aggregator_spec_adj_lines_func_from_string_representation(
        cmd_inv_as_str: str,
        is_implemented: bool= False) -> AggregatorSpec:
    return AggregatorSpecFuncStringRepresentation(kind=AggregatorKindEnum.ADJ_LINES_FUNC,
                                                  cmd_inv_as_str=cmd_inv_as_str,
                                                  is_implemented=is_implemented)

def make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(
        flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
        # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
        is_implemented: bool = False) -> AggregatorSpec:
    return AggregatorSpecFuncTransformer(kind=AggregatorKindEnum.CUSTOM_2_ARY,
                                         flag_option_list_transformer=flag_option_list_transformer,
                                         # pos_config_list_transformer=pos_config_list_transformer,
                                         is_implemented=is_implemented)

def make_aggregator_spec_custom_2_ary_from_string_representation(
        cmd_inv_as_str: str,
        is_implemented: bool = False) -> AggregatorSpec:
    return AggregatorSpecFuncStringRepresentation(kind=AggregatorKindEnum.CUSTOM_2_ARY,
                                                  cmd_inv_as_str=cmd_inv_as_str,
                                                  is_implemented=is_implemented)

def make_aggregator_spec_custom_n_ary_from_cmd_inv_with_transformers(
        flag_option_list_transformer: Optional[TransformerFlagOptionList] = None,
        # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
        is_implemented: bool = False) -> AggregatorSpec:
    return AggregatorSpecFuncTransformer(kind=AggregatorKindEnum.CUSTOM_N_ARY,
                                         flag_option_list_transformer=flag_option_list_transformer,
                                         # pos_config_list_transformer=pos_config_list_transformer,
                                         is_implemented=is_implemented)

def make_aggregator_spec_custom_n_ary_from_string_representation(
        cmd_inv_as_str: str,
        is_implemented: bool = False) -> AggregatorSpec:
    return AggregatorSpecFuncStringRepresentation(kind=AggregatorKindEnum.CUSTOM_N_ARY,
                                                  cmd_inv_as_str=cmd_inv_as_str,
                                                  is_implemented=is_implemented)

def return_aggregator_conc_if_none_else_itself(arg: Optional[AggregatorSpec]) -> AggregatorSpec:
    return return_default_if_none_else_itself(arg, make_aggregator_spec_concatenate())



class AggregatorSpecNonFunc(AggregatorSpec):

    def __init__(self,
                 kind: Literal[AggregatorKindEnum.CONCATENATE, AggregatorKindEnum.ADJ_LINES_MERGE, AggregatorKindEnum.ADJ_LINES_SEQ],
                 is_implemented: bool) -> None:
        AggregatorSpec.__init__(self, kind, is_implemented)

    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIOVars,
                       inputs_from: List[Union[IOVar, ArgStringType]],
                       # ArgStringType needed for typing, only IOVar provided
                       output_to: IOVar
                       ) -> Optional[Aggregator]:
        if not self.is_implemented:
            return None
        if self.kind == AggregatorKindEnum.CONCATENATE:
            cmd_inv_cat = CommandInvocationWithIOVars.make_cat_command_invocation_with_io_vars(inputs_from, output_to)
            return Aggregator.make_aggregator_from_cmd_inv_with_io(cmd_inv_cat, self.kind)
        elif self.kind == AggregatorKindEnum.ADJ_LINES_MERGE:
            assert(len(inputs_from) == 1)
            assert(False)
            # TODO
            # tr -d '\n' | sed '$a\' seems to do the job -> @KK: Can we join this in one command so no sequence of commands?
            return None
        elif self.kind == AggregatorKindEnum.ADJ_LINES_SEQ:
            assert(len(inputs_from) == 1)
            assert(False)
            # TODO
            return None

    def get_actual_2_ary_aggregator_with_aux(self,
                                             fst_normal_input: FileNameOrStdDescriptor,
                                             fst_aux_inputs_from: List[FileNameOrStdDescriptor],
                                             snd_normal_input: FileNameOrStdDescriptor,
                                             snd_aux_inputs_from: List[FileNameOrStdDescriptor],
                                             output_to: FileNameOrStdDescriptor,
                                             aux_outputs_to: List[FileNameOrStdDescriptor]
                                             ):
        raise Exception("Auxiliary information from mapper to aggregator only supported for aggregators given as string")


class AggregatorSpecFuncTransformer(AggregatorSpec):

    def __init__(self,
                 kind: Literal[AggregatorKindEnum.ADJ_LINES_FUNC, AggregatorKindEnum.CUSTOM_2_ARY, AggregatorKindEnum.CUSTOM_N_ARY],
                 flag_option_list_transformer: Optional[TransformerFlagOptionList] = None, # None translates to same as seq
                 # pos_config_list_transformer: Optional[TransformerPosConfigList] = None,
                 is_implemented: bool=False) -> None:
        AggregatorSpec.__init__(self, kind, is_implemented)
        # for now, we keep everything in operand list as it is but substitute streaming input and output
        self.flag_option_list_transformer: TransformerFlagOptionList = \
            return_transformer_flagoption_list_same_as_seq_if_none_else_itself(flag_option_list_transformer)

    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIOVars,
                       inputs_from: List[Union[IOVar, ArgStringType]],
                       # ArgStringType needed for typing, only IOVar provided
                       output_to: IOVar
                       ) -> Optional[Aggregator]:
        if not self.is_implemented:
            return None
        # sanity checks
        if self.kind == AggregatorKindEnum.ADJ_LINES_FUNC:
            assert(len(inputs_from) == 1)
        elif self.kind == AggregatorKindEnum.CUSTOM_2_ARY:
            assert(len(inputs_from) == 2)
        aggregator_cmd_inv = deepcopy(original_cmd_invocation)
        aggregator_cmd_inv.flag_option_list = self.flag_option_list_transformer.get_flag_option_list_after_transformer_application(original_cmd_invocation.flag_option_list)
        # access map modifications
        # Hard-coded how to provide input and get output -> TODO: move to spec
        aggregator_cmd_inv.remove_streaming_inputs()
        aggregator_cmd_inv.operand_list = inputs_from
        for input_id in inputs_from:
            assert not input_id in aggregator_cmd_inv.access_map and isinstance(input_id, IOVar)
            aggregator_cmd_inv.access_map[input_id] = make_stream_input()
        aggregator_cmd_inv.replace_var(aggregator_cmd_inv.implicit_use_of_streaming_output, output_to)
        return Aggregator.make_aggregator_from_cmd_inv_with_io(aggregator_cmd_inv, self.kind)

    def get_actual_2_ary_aggregator_with_aux(self,
                                             fst_normal_input: FileNameOrStdDescriptor,
                                             fst_aux_inputs_from: List[FileNameOrStdDescriptor],
                                             snd_normal_input: FileNameOrStdDescriptor,
                                             snd_aux_inputs_from: List[FileNameOrStdDescriptor],
                                             output_to: FileNameOrStdDescriptor,
                                             aux_outputs_to: List[FileNameOrStdDescriptor]
                                             ):
        raise Exception("Auxiliary information from mapper to aggregator only supported for aggregators given as string")


class AggregatorSpecFuncStringRepresentation(AggregatorSpec):

    def __init__(self,
                 kind: Literal[AggregatorKindEnum.ADJ_LINES_FUNC, AggregatorKindEnum.CUSTOM_2_ARY, AggregatorKindEnum.CUSTOM_N_ARY],
                 cmd_inv_as_str: str,
                 is_implemented: bool=False) -> None:
        AggregatorSpec.__init__(self, kind, is_implemented)
        # for now, we keep everything in operand list as it is but substitute streaming input and output
        self.cmd_inv_as_str = cmd_inv_as_str

    def get_aggregator(self,
                       original_cmd_invocation: CommandInvocationWithIOVars,
                       inputs_from: List[Union[IOVar, ArgStringType]],
                       # ArgStringType needed for typing, only IOVar provided
                       output_to: IOVar
                       ) -> Optional[Aggregator]:
        if not self.is_implemented:
            return None
        agg_cmd_inv = parse(self.cmd_inv_as_str)
        # currently, we assume no file names in option arguments
        # this is why we do not convert them properly but need to do this trick for typing
        # later, if option arguments contain file names, they need to get IOVar from PaSh
        new_flagoption_list : List[Union[Flag, OptionWithIOVar]] = []
        for x in agg_cmd_inv.flag_option_list:
            assert isinstance(x, Flag)
            new_flagoption_list.append(x)
        # Assumption: inputs are given as operands and output is stdout
        # Assumption: no inputs or outputs given (also as config) since we do not do access map things etc...
        access_map = {input_id: make_stream_input() for input_id in inputs_from}
        access_map[output_to] = make_stream_output()
        agg_cmd_inv_with_io_vars = Aggregator(kind=self.kind,
                                              access_map=access_map,
                                              cmd_name = agg_cmd_inv.cmd_name,
                                              flag_option_list=new_flagoption_list,
                                              operand_list=inputs_from,
                                              implicit_use_of_streaming_input=None,
                                              implicit_use_of_streaming_output=output_to)
        if self.kind == AggregatorKindEnum.ADJ_LINES_FUNC:
            assert(len(inputs_from) == 1)
            # TODO: isn't it 2 here?
            raise Exception("case not yet implemented")
        elif self.kind == AggregatorKindEnum.CUSTOM_2_ARY:
            assert(len(inputs_from) == 2)
        return agg_cmd_inv_with_io_vars

    def get_actual_2_ary_aggregator_with_aux(self,
                                             fst_normal_input: IOVar,
                                             fst_aux_inputs_from: List[IOVar],
                                             snd_normal_input: IOVar,
                                             snd_aux_inputs_from: List[IOVar],
                                             output_to: IOVar,
                                             aux_outputs_to: List[IOVar]
                                             ):
        assert(len(fst_aux_inputs_from) == len(snd_aux_inputs_from))
        assert(len(fst_aux_inputs_from) == len(aux_outputs_to))
        agg_cmd_inv = parse(self.cmd_inv_as_str)
        # currently, we assume no file names in option arguments
        # this is why we do not convert them properly but need to do this trick for typing
        # later, if option arguments contain file names, they need to get IOVar from PaSh
        new_flagoption_list : List[Union[Flag, OptionWithIOVar]] = []
        for x in agg_cmd_inv.flag_option_list:
            assert isinstance(x, Flag)
            new_flagoption_list.append(x)
        all_inputs = [fst_normal_input] + fst_aux_inputs_from + [snd_normal_input] + snd_aux_inputs_from
        all_outputs = [output_to] + aux_outputs_to
        access_map = dict()
        for input_id in all_inputs:
            access_map[input_id] = make_stream_input()
        for output_id in all_outputs:
            access_map[output_id] = make_stream_output()
        new_operand_list : List[Union[ArgStringType, IOVar]] = []
        # trick for typing...
        for x in [fst_normal_input] + fst_aux_inputs_from + [snd_normal_input] + snd_aux_inputs_from + [output_to] + aux_outputs_to:
            new_operand_list.append(x)
        agg_cmd_inv_with_io_vars = Aggregator(kind=self.kind,
                                              access_map=access_map,
                                              cmd_name = agg_cmd_inv.cmd_name,
                                              flag_option_list=new_flagoption_list,
                                              operand_list=new_operand_list,
                                              implicit_use_of_streaming_input=None,
                                              implicit_use_of_streaming_output=None)
        return agg_cmd_inv_with_io_vars
