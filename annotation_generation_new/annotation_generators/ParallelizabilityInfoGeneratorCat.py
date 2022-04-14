from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.MapperSpec import MapperSpec, AdditionalInfoFromSplitter
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec


class ParallelizabilityInfoGeneratorCat(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # in general it is easily parallelizable, with the following exception:
    # -n which numbers output lines and -s which squeezes repeated empty output lines
    # -b which numbers non-blank lines
    # for -n without -s, we can parallelize with some a custom mapper (given the offset from which to count)
    # for -n and -s, we could only do with a 2nd pass so we omit this for now

    def generate_info(self) -> None:
        if not self.does_number_non_empty_output_lines():
            # Case analysis on combinations of squeeze and numbering all output lines
            if not self.does_squeeze_repeated_empty_output_lines() and not self.does_number_all_output_lines():
                self.append_to_parallelizer_list_if_seq_conc()
                self.append_to_parallelizer_list_rr_seq_conc()
            elif not self.does_squeeze_repeated_empty_output_lines() and self.does_number_all_output_lines():
                # we can have mappers that take offset as argument and without -s, this is stable
                mapper_spec = MapperSpec.make_mapper_spec_custom(spec_mapper_cmd_name='cat_offset_n_add_input',
                                                                 add_info_from_splitter=AdditionalInfoFromSplitter.LINE_NUM_OFFSET,
                                                                 is_implemented=False)
                parallelizer_if_cus_conc = Parallelizer.make_parallelizer_indiv_files(mapper_spec=mapper_spec)
                self.append_to_parallelizer_list(parallelizer_if_cus_conc)
                parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper_spec=mapper_spec)
                self.append_to_parallelizer_list(parallelizer_rr_cus_conc)
            elif self.does_squeeze_repeated_empty_output_lines() and not self.does_number_all_output_lines():
                # not numbered (in any way) but need to compare adjacent lines and possibly remove one blank line
                aggregator_spec = AggregatorSpec.make_aggregator_spec_adj_lines_func(spec_agg_cmd_name='merge_2_blank_lines_to_1',
                                                                                     is_implemented=False)
                parallelizer_if_seq_adjf = Parallelizer.make_parallelizer_indiv_files(aggregator_spec=aggregator_spec)
                self.append_to_parallelizer_list(parallelizer_if_seq_adjf)
                parallelizer_rr_seq_adjf = Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
                self.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
            elif self.does_squeeze_repeated_empty_output_lines() and self.does_number_all_output_lines():
                # parallelizable only with 2nd pass
                pass
        else:
            # parallelizable only with 2nd pass
            pass


    # private helper functions for conditions
    def does_squeeze_repeated_empty_output_lines(self):
        return self.does_flag_option_list_contains_at_least_one_of(["-s"])

    def does_number_non_empty_output_lines(self): # -b overwrites -n
        return self.does_flag_option_list_contains_at_least_one_of(["-b"])

    def does_number_all_output_lines(self):
        return self.does_flag_option_list_contains_at_least_one_of(["-n"])
