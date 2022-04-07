from __future__ import annotations
from typing import Optional

from enum import Enum
from util import standard_eq

from datatypes.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation.datatypes.parallelizability.Splitter import Splitter
from annotation_generation.datatypes.parallelizability.MapperSpec import MapperSpec
from annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorSpec
from annotation_generation.datatypes.parallelizability.Mapper import Mapper
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator

class AdditionalInfoMapperSpecToAggregator(Enum):
    NO_ADD_INPUT = 'no_add_input'

class Parallelizer:

    def __init__(self,
                 splitter: Splitter,
                 # , we only store MapperSpec and AggregatorSpec, actual ones to be retrieved with CMDInvPref in Pash
                 core_mapper_spec: MapperSpec,
                 core_aggregator_spec: AggregatorSpec,
                 info_mapper_aggregator: AdditionalInfoMapperSpecToAggregator = AdditionalInfoMapperSpecToAggregator.NO_ADD_INPUT
                 ) -> None:
        self.splitter: Splitter = splitter
        self.core_mapper_spec: MapperSpec = core_mapper_spec
        self.core_aggregator_spec: AggregatorSpec = core_aggregator_spec
        self.info_mapper_aggregator = info_mapper_aggregator

    def __eq__(self, other: Parallelizer) -> bool:
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

    def get_actual_mapper(self, cmd_invocation_prefix: CommandInvocationPrefix) -> Optional[Mapper]:
        return self.core_mapper_spec.get_mapper(cmd_invocation_prefix)

    def get_aggregator_spec(self) -> AggregatorSpec:
        return self.core_aggregator_spec

    def get_actual_aggregator(self, cmd_invocation_prefix: CommandInvocationPrefix) -> Optional[Aggregator]:
        return self.core_aggregator_spec.get_aggregator(cmd_invocation_prefix)

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
    # TODO: rename
    def make_parallelizer_consec_junks(mapper_spec: Optional[MapperSpec]=None,
                                       aggregator_spec: Optional[AggregatorSpec]=None
                                       ) -> Parallelizer:
        mapper_spec = MapperSpec.return_mapper_spec_seq_if_none_else_itself(mapper_spec)
        aggregator_spec = AggregatorSpec.return_aggregator_conc_if_none_else_itself(aggregator_spec)
        return Parallelizer(Splitter.make_splitter_consec_chunks(), mapper_spec, aggregator_spec)
