from copy import deepcopy
from typing import Optional, List, Union

from datatypes_new.CommandInvocationWithIOVars import CommandInvocationWithIOVars
from util_standard import standard_eq
from util_new import return_default_if_none_else_itself

from datatypes_new.BasicDatatypesWithIOVar import IOVar
from datatypes_new.BasicDatatypes import FileNameOrStdDescriptor, ArgStringType
from annotation_generation_new.datatypes.parallelizability.Splitter import Splitter, make_splitter_consec_chunks, \
    make_splitter_indiv_files, make_splitter_round_robin, make_splitter_round_robin_with_unwrap
from annotation_generation_new.datatypes.parallelizability.MapperSpec import MapperSpec, \
    return_mapper_spec_seq_if_none_else_itself
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec, \
    return_aggregator_conc_if_none_else_itself
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator

from enum import Enum

# this will probably become its own class with more information later
class AdditionalInfoSplitterToMapper(Enum):
    NO_ADD_INPUT = 'no_add_input'
    LINE_NUM_OFFSET = 'line_num_offset'
    BYTE_OFFSET = 'byte_offset'
    LINE_NUM_AND_BYTE_OFFSET = 'line_num_and_byte_offset'


class Parallelizer:

    def __init__(self,
                 splitter: Splitter,
                 # , we only store MapperSpec and AggregatorSpec, actual ones to be retrieved with CMDInvPref in Pash
                 core_mapper_spec: MapperSpec,
                 core_aggregator_spec: AggregatorSpec,
                 info_splitter_mapper: Optional[AdditionalInfoSplitterToMapper],
                 info_mapper_aggregator: int # the number of pipes to connect
                 # if this is
                 ) -> None:
        self.splitter: Splitter = splitter
        self.core_mapper_spec: MapperSpec = core_mapper_spec
        self.core_aggregator_spec: AggregatorSpec = core_aggregator_spec
        self.info_splitter_mapper: AdditionalInfoSplitterToMapper = return_default_if_none_else_itself(info_splitter_mapper, AdditionalInfoSplitterToMapper.NO_ADD_INPUT)
        self.info_mapper_aggregator = info_mapper_aggregator
        # sanity check that round robin is only applied with following aggregators:
        if self.splitter.is_splitter_round_robin():
            assert(self.core_aggregator_spec.is_aggregator_spec_concatenate() or
                   self.core_aggregator_spec.is_aggregator_spec_adj_lines_merge() or
                   self.core_aggregator_spec.is_aggregator_spec_adj_lines_seq() or
                   self.core_aggregator_spec.is_aggregator_spec_adj_lines_func())

    def __eq__(self, other) -> bool:
        return standard_eq(self, other)

    def __repr__(self) -> str:
        return f'Parallizer: \n' \
               f'splitter: {self.splitter} \n' \
               f'mapper attr: {self.core_mapper_spec} \n' \
               f'aggregator attr: {self.core_aggregator_spec} \n'

    def get_splitter(self) -> Splitter:
        return self.splitter

    def get_mapper_spec(self) -> MapperSpec:
        return self.core_mapper_spec

    def get_actual_mapper(self,
                          cmd_invocation: CommandInvocationWithIOVars,
                          input_from: IOVar,
                          output_to: IOVar,
                          aux_output_tos: List[IOVar]) \
            -> Optional[Mapper]:
        assert(len(aux_output_tos) == self.info_mapper_aggregator)
        return self.core_mapper_spec.get_mapper(cmd_invocation, input_from, output_to, aux_output_tos)

    def get_aggregator_spec(self) -> AggregatorSpec:
        return self.core_aggregator_spec

    def get_actual_aggregator(self,
                              cmd_invocation: CommandInvocationWithIOVars,
                              inputs_from: List[Union[IOVar, ArgStringType]],
                              # ArgStringType needed for typing, only IOVar provided
                              output_to: IOVar
                            ) -> Optional[Aggregator]:
        return self.core_aggregator_spec.get_aggregator(cmd_invocation, inputs_from, output_to)

    def get_actual_2_ary_aggregator_with_aux(self,
                                            fst_normal_input: FileNameOrStdDescriptor,
                                            fst_aux_inputs_from: List[FileNameOrStdDescriptor],
                                            snd_normal_input: FileNameOrStdDescriptor,
                                            snd_aux_inputs_from: List[FileNameOrStdDescriptor],
                                            output_to: FileNameOrStdDescriptor,
                                            aux_outputs_to: List[FileNameOrStdDescriptor]
                                            ):
        return self.core_aggregator_spec.get_actual_2_ary_aggregator_with_aux(fst_normal_input, fst_aux_inputs_from,
                                                                              snd_normal_input, snd_aux_inputs_from,
                                                                              output_to, aux_outputs_to)

    def get_info_mapper_aggregator(self) -> int:
        return self.info_mapper_aggregator

    def are_all_parts_implemented(self):
        return self.core_mapper_spec.is_implemented and self.core_aggregator_spec.is_implemented

def make_parallelizer_indiv_files(mapper_spec: Optional[MapperSpec]=None,
                                  aggregator_spec: Optional[AggregatorSpec]=None,
                                  info_splitter_mapper: Optional[AdditionalInfoSplitterToMapper]=None,
                                  info_mapper_aggregator: int = 0
                                  ) -> Parallelizer:
    mapper_spec = return_mapper_spec_seq_if_none_else_itself(mapper_spec)
    aggregator_spec = return_aggregator_conc_if_none_else_itself(aggregator_spec)
    return Parallelizer(make_splitter_indiv_files(), mapper_spec, aggregator_spec, info_splitter_mapper, info_mapper_aggregator)

def make_parallelizer_round_robin(mapper_spec: Optional[MapperSpec]=None,
                                  aggregator_spec: Optional[AggregatorSpec]=None,
                                  info_splitter_mapper: Optional[AdditionalInfoSplitterToMapper]=None,
                                  info_mapper_aggregator: int = 0
                                  ) -> Parallelizer:
    mapper_spec = return_mapper_spec_seq_if_none_else_itself(mapper_spec)
    aggregator_spec = return_aggregator_conc_if_none_else_itself(aggregator_spec)
    return Parallelizer(make_splitter_round_robin(), mapper_spec, aggregator_spec, info_splitter_mapper, info_mapper_aggregator)

def make_parallelizer_round_robin_with_unwrap_from_other(parallelizer):
    new_parallelizer = deepcopy(parallelizer)
    new_parallelizer.splitter = make_splitter_round_robin_with_unwrap()
    return new_parallelizer

def make_parallelizer_consec_chunks(mapper_spec: Optional[MapperSpec]=None,
                                    aggregator_spec: Optional[AggregatorSpec]=None,
                                    info_splitter_mapper: Optional[AdditionalInfoSplitterToMapper] = None,
                                    info_mapper_aggregator: int = 0
                                    ) -> Parallelizer:
    mapper_spec = return_mapper_spec_seq_if_none_else_itself(mapper_spec)
    aggregator_spec = return_aggregator_conc_if_none_else_itself(aggregator_spec)
    return Parallelizer(make_splitter_consec_chunks(), mapper_spec, aggregator_spec, info_splitter_mapper, info_mapper_aggregator)
