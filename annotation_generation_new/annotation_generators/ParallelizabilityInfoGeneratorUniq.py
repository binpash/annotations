from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.Parallelizer import \
    make_parallelizer_round_robin, make_parallelizer_consec_chunks
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_adj_lines_func_from_string_representation


class ParallelizabilityInfoGeneratorUniq(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-D", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--all-repeated", "-f", "--group", "-s", "-w"]

    # Which ones do affect parallelizability?
    # base-line: parallelization possible with RR/(CC) x SEQ x ADJF
    # by using the sequential command for ADJF, we handle a lot of cases where flags contain semantic information
    # -d, -D and --all-repeated renders parallelization infeasible (at least very hard)
    # -c makes it harder but feasible:
    #   one needs to cut the prefix of numbers, run the sequential and see whether it is merged
    # TODO: what does --group do?

    def generate_info(self) -> None:
        # check for flags/options that make it hard to parallelize
        if not self.does_flag_option_list_contain_at_least_one_of(["-d", "-D", "--all-repeated"]):
            if self.does_flag_option_list_contain_at_least_one_of(["-c"]):
                # we need a special merge
                aggregator_spec = make_aggregator_spec_adj_lines_func_from_string_representation(cmd_inv_as_str='PLACEHOLDER:uniq_merge_count_uniq', is_implemented=False)
                parallelizer_cc_seq_adjf = make_parallelizer_consec_chunks(aggregator_spec=aggregator_spec)
                parallelizer_rr_seq_adjf = make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
                self.append_to_parallelizer_list(parallelizer_cc_seq_adjf)
                self.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
            else:
                # just apply the sequential command to the last and first line
                self.append_to_parallelizer_list_cc_seq_adjs()
                self.append_to_parallelizer_list_rr_seq_adjs()
