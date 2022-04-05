from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorSpec


class ParallelizabilityInfoGeneratorUniq(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-D", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--all-repeated", "-f", "--group", "-s", "-w"]

    # Which ones do affect parallelizability?
    # base-line: parallelization possible with RR/(CJ) x SEQ x ADJF
    # by using the sequential command for ADJF, we handle a lot of cases where flags contain semantic information
    # -d, -D and --all-repeated renders parallelization infeasible (at least very hard)
    # -c makes it harder but feasible:
    #   one needs to cut the prefix of numbers, run the sequential and see whether it is merged
    # TODO: what does --group do?

    def generate_info(self) -> None:
        # check for flags/options that make it super hard
        if not self.does_flag_option_list_contains_at_least_one_of(["-d", "-D", "--all-repeated"]):
            if self.does_flag_option_list_contains_at_least_one_of(["-c"]):
                # we need a special merge
                aggregator_spec = AggregatorSpec.make_aggregator_adj_lines_func('todo_impl_merge_count_uniq', is_implemented=False)
                parallelizer_rr_seq_adjf = Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
                self.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
            else:
                # just apply the sequential command to the last and first line
                self.append_to_parallelizer_list_rr_seq_adjs()




