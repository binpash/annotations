from __future__ import annotations
from typing import Optional

from enum import Enum

from datatypes.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation.datatypes.parallelizability.Splitter import Splitter
from annotation_generation.datatypes.parallelizability.MapperSpec import MapperSpec
from annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorSpec
from annotation_generation.datatypes.parallelizability.Mapper import Mapper
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator

class AdditionalInfoSplitterToMapper(Enum):
    NO_ADD_INPUT = 0

class AdditionalInfoMapperSpecToAggregator(Enum):
    NO_ADD_INPUT = 0

class Parallelizer:

    # here, we only store MapperSpec and AggregatorSpec, actual ones to be retrieved with CMDInvPref in Pash
    def __init__(self,
                 splitter: Splitter,
                 core_mapper: MapperSpec,
                 core_aggregator: AggregatorSpec,
                 info_splitter_mapper: AdditionalInfoSplitterToMapper = AdditionalInfoSplitterToMapper.NO_ADD_INPUT,
                 info_mapper_aggregator: AdditionalInfoMapperSpecToAggregator = AdditionalInfoMapperSpecToAggregator.NO_ADD_INPUT
                 ) -> None:
        self.splitter: Splitter = splitter
        self.core_mapper_spec: MapperSpec = core_mapper
        self.core_aggregator_spec: AggregatorSpec = core_aggregator
        self.info_splitter_mapper: AdditionalInfoSplitterToMapper = info_splitter_mapper
        self.info_mapper_aggregator = info_mapper_aggregator

    def __eq__(self, other: Parallelizer) -> bool:
        return self.splitter == other.splitter \
               and self.core_mapper_spec == other.core_mapper_spec \
               and self.core_aggregator_spec == other.core_aggregator_spec \
               and self.info_splitter_mapper == other.info_splitter_mapper \
               and self.info_mapper_aggregator == other.info_mapper_aggregator

    def __repr__(self) -> str:
        return f'Parallizer: \n' \
               f'splitter: {self.splitter} \n' \
               f'mapper attr: {self.core_mapper_spec} \n' \
               f'aggregator attr: {self.core_aggregator_spec} \n'

    def get_splitter(self) -> Splitter:
        return self.splitter

    def get_mapper_spec(self) -> MapperSpec:
        return self.core_mapper_spec

    def get_actual_mapper(self, cmd_invocation_prefix: CommandInvocationPrefix) -> Optional[Mapper]:
        return self.core_mapper_spec.get_mapper(cmd_invocation_prefix)

    def get_aggregator_spec(self) -> AggregatorSpec:
        return self.core_aggregator_spec

    def get_actual_aggregator(self, cmd_invocation_prefix: CommandInvocationPrefix) -> Optional[Aggregator]:
        return self.core_aggregator_spec.get_aggregator(cmd_invocation_prefix)

    def get_info_splitter_mapper(self) -> AdditionalInfoSplitterToMapper:
        return self.info_splitter_mapper

    def get_info_mapper_aggregator(self) -> AdditionalInfoMapperSpecToAggregator:
        return self.info_mapper_aggregator

    @staticmethod
    def make_parallelizer_indiv_files(mapper_spec: Optional[MapperSpec]=None,
                                      aggregator_spec: Optional[AggregatorSpec]=None
                                      ) -> Parallelizer:
        mapper_spec = MapperSpec.return_mapper_spec_seq_if_none_else_itself(mapper_spec)
        aggregator_spec = AggregatorSpec.return_aggregator_conc_if_none_else_itself(aggregator_spec)
        return Parallelizer(Splitter.make_splitter_indiv_files(), mapper_spec, aggregator_spec)

    @staticmethod
    def make_parallelizer_round_robin(mapper_spec: Optional[MapperSpec]=None,
                                      aggregator_spec: Optional[AggregatorSpec]=None
                                      ) -> Parallelizer:
        mapper_spec = MapperSpec.return_mapper_spec_seq_if_none_else_itself(mapper_spec)
        aggregator_spec = AggregatorSpec.return_aggregator_conc_if_none_else_itself(aggregator_spec)
        return Parallelizer(Splitter.make_splitter_round_robin(), mapper_spec, aggregator_spec)

    @staticmethod
    def make_parallelizer_consec_junks(mapper_spec: Optional[MapperSpec]=None,
                                       aggregator_spec: Optional[AggregatorSpec]=None
                                       ) -> Parallelizer:
        mapper_spec = MapperSpec.return_mapper_spec_seq_if_none_else_itself(mapper_spec)
        aggregator_spec = AggregatorSpec.return_aggregator_conc_if_none_else_itself(aggregator_spec)
        return Parallelizer(Splitter.make_splitter_consec_junks(), mapper_spec, aggregator_spec)
