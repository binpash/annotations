from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.Mapper import Mapper
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator


class ParallelizabilityInfoGeneratorGrep(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-V", "--help", "-E", "-F", "-G", "-P", "-i", "--no-ignore-case", "-v", "-w",
    #                      "-x", "-y", "-c", "-L", "-l", "-o", "-q", "-s", "-b", "-H", "-h", "-n", "-T", "-Z",
    #                      "--no-group-separator", "-a", "-I", "-r", "-R", "--line-buffered", "-U", "-z"]
    # list_of_all_options = ["-e", "-f", "--color", "-m", "--label", "-A", "-B", "-C", "--group-separator",
    #                        "--binary-files", "-D", "-d", "--exclude", "--exclude-from", "--exclude-dir", "--include"]

    # Which ones do affect parallelizability?
    # -c, -L, -l, -b, -n;
    # by checking, -L and -l overrule -c overrule -b and -n; output of -n always precedes output of -b
    # assumption: RR not over file boundaries
    # and -A, -B, and -C but we do not parallelize within file boundaries since they require context
    # for -q, the input is not read further after some condition is met, so we do not parallelize at all
    # for -m, we only do IF

    def generate_info(self) -> None:
        # TODO
        pass

    def apply_transformers_for_parallelizers(self) -> None:
        if not self.does_flag_option_list_contains_at_least_one_of(["-q"]):
            parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
            self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
            if not self.does_flag_option_list_contains_at_least_one_of(["-A", "-B", "-C", "-m"]):
                if self.does_flag_option_list_contains_at_least_one_of(["-L", "-l"]):
                    aggregator = Aggregator.make_aggregator_custom_2_ary("merge_keeping_longer_output")
                    parallelizer_rr_seq_cus2 = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_seq_cus2)
                    # the output for both options is either empty or the filename (same for both if so)
                    # for "-l": if there was a match in one part, the filename will propagate; if not, not
                    # for "-L": if there was no match in one part, the filename will propagate; it not, not
                elif self.does_flag_option_list_contains_at_least_one_of(["-c"]):
                    aggregator = Aggregator.make_aggregator_custom_2_ary("sum_indiv_results_up")
                    parallelizer_rr_seq_cus2 = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_seq_cus2)
                elif self.does_flag_option_list_contains_at_least_one_of(["-n"]) and self.does_flag_option_list_contains_at_least_one_of(["-b"]):
                    mapper = Mapper.make_mapper_custom("add_line_number_and_byte_offset")
                    parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
                elif self.does_flag_option_list_contains_at_least_one_of(["-n"]):
                    mapper = Mapper.make_mapper_custom("add_line_number_offset")
                    parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
                elif self.does_flag_option_list_contains_at_least_one_of(["-b"]):
                    mapper = Mapper.make_mapper_custom("add_byte_offset")
                    parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
                else:   # none of the above affecting flags
                    parallelizer_rr_seq_conc = Parallelizer.make_parallelizer_round_robin()
                    self.meta.append_to_parallelizer_list(parallelizer_rr_seq_conc)
