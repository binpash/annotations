from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.MapperSpec import MapperSpec
from annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorSpec


class ParallelizabilityInfoGeneratorCat(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # in general it is easily parallelizable, with the following exception:
    # -n which numbers output lines and -s which squeezes repeated empty output lines
    # for -n without -s, we can parallelize with some a custom mapper (given the offset from which to count)
    # for -n and -s, we could only do with a 2nd pass so we omit this for now

    def generate_info(self) -> None:
        if self.does_flag_option_list_contains_at_least_one_of(["-n"]) and not self.does_flag_option_list_contains_at_least_one_of(["-s"]):
            pass
            # we can have mappers that take offset as argument and without -s, this is stable
                # TODO: mapper needs special additional input
                #       maybe rather in MapperSpec and Mapper than Parallelizer: what and how?
                # mapper_spec = MapperSpec.make_mapper_spec_custom(spec_mapper_cmd_name='todo_impl_offset_n_add_input', is_implemented=False)
                # parallelizer_if_cus_conc = Parallelizer.make_parallelizer_indiv_files(mapper_spec)
                # self.append_to_parallelizer_list(parallelizer_if_cus_conc)
                # parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper_spec)
                # self.append_to_parallelizer_list(parallelizer_rr_cus_conc)
        elif not self.does_flag_option_list_contains_at_least_one_of(["-n"]) and self.does_flag_option_list_contains_at_least_one_of(["-s"]):
                # not numbered but need to compare adjacent lines and possibly remove one blank line
                aggregator_spec = AggregatorSpec.make_aggregator_adj_lines_func('todo_impl_merge_2blanks_to_1', is_implemented=False)
                parallelizer_if_seq_adjf = Parallelizer.make_parallelizer_indiv_files(aggregator_spec)
                self.append_to_parallelizer_list(parallelizer_if_seq_adjf)
                parallelizer_rr_seq_adjf = Parallelizer.make_parallelizer_round_robin(aggregator_spec)
                self.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
        elif not self.does_flag_option_list_contains_at_least_one_of(["-n"]) and not self.does_flag_option_list_contains_at_least_one_of(["-s"]):
                # add two parallelizers: IF and RR with SEQ and CONC each
                self.append_to_parallelizer_list_if_seq_conc()
                self.append_to_parallelizer_list_rr_seq_conc()
