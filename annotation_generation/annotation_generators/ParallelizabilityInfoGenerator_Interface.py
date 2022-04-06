from __future__ import annotations
from typing import List, Optional

from abc import ABC, abstractmethod

from Generator_Interface import Generator_Interface
from datatypes.CommandInvocation import CommandInvocation
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.Splitter import Splitter
from annotation_generation.datatypes.parallelizability.MapperSpec import MapperSpec
from annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorSpec
from annotation_generation.datatypes.ParallelizabilityInfo import ParallelizabilityInfo


class ParallelizabilityInfoGeneratorInterface(Generator_Interface, ABC):

    # This is the select_subcommand from the original proposal,
    #   instead of returning functions, it initializes the object
    #   and then we can call its methods.
    def __init__(self, cmd_invocation: CommandInvocation) -> None:
        super().__init__(cmd_invocation=cmd_invocation)
        self.parallelizability_info: ParallelizabilityInfo = ParallelizabilityInfo()

    @abstractmethod
    def generate_info(self) -> None:
        # info to provide: parallelizer_list, round_robin_comp_with_cat, is_commutative (for optimisations)
        # TODO: add info about RR_cat and is_comm in existent generators
        pass

    def get_info(self) -> ParallelizabilityInfo:
        return self.parallelizability_info


    ## HELPERS/Library functions: modifying parallelizability info

    def append_to_parallelizer_list(self, parallelizer: Parallelizer) -> None:
        self.parallelizability_info.append_to_parallelizer_list(parallelizer)

    def append_to_parallelizer_list_if_seq_conc(self) -> None:
        parallelizer_if_seq_conc: Parallelizer = Parallelizer.make_parallelizer_indiv_files()
        self.append_to_parallelizer_list(parallelizer_if_seq_conc)

    def append_to_parallelizer_list_if_seq_adjm(self) -> None:
        aggregator_spec = AggregatorSpec.make_aggregator_adj_lines_merge()
        parallelizer_rr_seq_adjm = Parallelizer.make_parallelizer_indiv_files(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_rr_seq_adjm)

    def append_to_parallelizer_list_rr_seq_conc(self) -> None:
        parallelizer_rr_seq_conc: Parallelizer = Parallelizer.make_parallelizer_round_robin()
        self.append_to_parallelizer_list(parallelizer_rr_seq_conc)

    def append_to_parallelizer_list_rr_seq_adjm(self) -> None:
        aggregator_spec = AggregatorSpec.make_aggregator_adj_lines_merge()
        parallelizer_rr_seq_adjm = Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_rr_seq_adjm)

    def append_to_parallelizer_list_rr_seq_adjs(self) -> None:
        aggregator_spec = AggregatorSpec.make_aggregator_adj_lines_seq()
        parallelizer_rr_seq_adjs = Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_rr_seq_adjs)
