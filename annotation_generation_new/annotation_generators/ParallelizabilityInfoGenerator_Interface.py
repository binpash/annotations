from abc import ABC, abstractmethod

from datatypes_new.CommandInvocationInitial import CommandInvocationInitial

from annotation_generation_new.annotation_generators.Generator_Interface import Generator_Interface

from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer, \
    make_parallelizer_indiv_files, make_parallelizer_consec_chunks, make_parallelizer_round_robin
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec, \
    make_aggregator_spec_adj_lines_merge, make_aggregator_spec_adj_lines_seq, make_aggregator_spec_adj_lines_func_from_string_representation
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo


class ParallelizabilityInfoGeneratorInterface(Generator_Interface, ABC):

    def __init__(self, cmd_invocation: CommandInvocationInitial) -> None:
        self.cmd_inv = cmd_invocation
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
        parallelizer_if_seq_conc: Parallelizer = make_parallelizer_indiv_files()
        self.append_to_parallelizer_list(parallelizer_if_seq_conc)

    def append_to_parallelizer_list_if_seq_adjm(self) -> None:
        aggregator_spec = make_aggregator_spec_adj_lines_merge()
        parallelizer_rr_seq_adjm = make_parallelizer_indiv_files(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_rr_seq_adjm)

    def append_to_parallelizer_list_cc_seq_conc(self) -> None:
        parallelizer_cc_seq_conc: Parallelizer = make_parallelizer_consec_chunks()
        self.append_to_parallelizer_list(parallelizer_cc_seq_conc)

    def append_to_parallelizer_list_cc_seq_adjm(self) -> None:
        aggregator_spec = make_aggregator_spec_adj_lines_merge()
        parallelizer_cc_seq_adjm = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_adjm)

    def append_to_parallelizer_list_rr_seq_conc(self) -> None:
        parallelizer_rr_seq_conc: Parallelizer = make_parallelizer_round_robin()
        self.append_to_parallelizer_list(parallelizer_rr_seq_conc)

    def append_to_parallelizer_list_rr_seq_adjm(self) -> None:
        aggregator_spec = make_aggregator_spec_adj_lines_merge()
        parallelizer_rr_seq_adjm = make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_rr_seq_adjm)

    def append_to_parallelizer_list_rr_seq_adjs(self) -> None:
        aggregator_spec = make_aggregator_spec_adj_lines_seq()
        parallelizer_rr_seq_adjs = make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_rr_seq_adjs)

    def append_to_parallelizer_list_cc_seq_adjs(self) -> None:
        aggregator_spec = make_aggregator_spec_adj_lines_seq()
        parallelizer_cc_seq_adjs = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_adjs)

    def append_to_parallelizer_list_rr_seq_adjf(self, string_repr_func: str, is_implemented: bool) -> None:
        aggregator_spec = make_aggregator_spec_adj_lines_func_from_string_representation(string_repr_func, is_implemented)
        parallelizer_rr_seq_adjs = make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_rr_seq_adjs)

    def append_to_parallelizer_list_cc_seq_adjf(self, string_repr_func: str, is_implemented: bool) -> None:
        aggregator_spec = make_aggregator_spec_adj_lines_func_from_string_representation(string_repr_func, is_implemented)
        parallelizer_cc_seq_adjs = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
        self.append_to_parallelizer_list(parallelizer_cc_seq_adjs)

    def set_commutative(self) -> None:
        self.parallelizability_info.set_commutative()
