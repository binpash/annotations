from annotation_generation_new.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from annotation_generation_new.datatypes.parallelizability.Parallelizer import \
    AdditionalInfoSplitterToMapper, make_parallelizer_round_robin, make_parallelizer_consec_chunks
from annotation_generation_new.datatypes.parallelizability.MapperSpec import make_mapper_spec_custom
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_string_representation


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
        if not self.does_flag_option_list_contain_at_least_one_of(["-q"]):
            # # for indiv files
            # self.append_to_parallelizer_list_if_seq_conc()
            # rest for round-robin
            mapper_spec = None
            aggregator_spec = None
            add_info_from_splitter = None
            # CA to decide which mapper or aggregator, parallelizer added after CA
            if not self.does_flag_option_list_contain_at_least_one_of(["-A", "-B", "-C", "-m"]):
                if self.does_flag_option_list_contain_at_least_one_of(["-L", "-l"]):
                    # the output for both options is either empty or the filename (same for both if so)
                    # for "-l": if there was a match in one part, the filename will propagate; if not, not
                    # for "-L": if there was no match in one part, the filename will propagate; it not, not
                    aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str='PLACEHOLDER:merge_keeping_longer_output',
                                                                                       is_implemented=False)
                elif self.does_flag_option_list_contain_at_least_one_of(["-c"]):
                    aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(cmd_inv_as_str='PLACEHOLDER:sum_indiv_results_up',
                                                                                       is_implemented=False)
                    # cat input1 input2 | paste -s -d + - | bc
                elif self.does_flag_option_list_contain_at_least_one_of(["-n"]) and self.does_flag_option_list_contain_at_least_one_of(["-b"]):
                    mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_line_number_and_byte_offset',
                                                                     is_implemented=False)
                    add_info_from_splitter=AdditionalInfoSplitterToMapper.LINE_NUM_AND_BYTE_OFFSET
                elif self.does_flag_option_list_contain_at_least_one_of(["-n"]):
                    mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_line_number_offset',
                                                                     is_implemented=False)
                    add_info_from_splitter=AdditionalInfoSplitterToMapper.LINE_NUM_OFFSET
                elif self.does_flag_option_list_contain_at_least_one_of(["-b"]):
                    mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_byte_offset',
                                                                     is_implemented=False)
                    add_info_from_splitter = AdditionalInfoSplitterToMapper.BYTE_OFFSET
                else:   # none of the above affecting flags
                    pass    #just keep mapper and aggregator None and thus add RR_SEQ_CONC
            # we exploit that mapper_spec becomes seq and aggregator_spec becomes conc if given None
            # check can be removed once all are implemented! (exploits short-circuiting)
            # TODO: we should be able to remove the `is_implemented`-check as it is checked later
            if (mapper_spec is None or mapper_spec.is_implemented) and \
                    (aggregator_spec is None or aggregator_spec.is_implemented):
                parallelizer_cc = make_parallelizer_consec_chunks(mapper_spec=mapper_spec,
                                                                  aggregator_spec=aggregator_spec,
                                                                  info_splitter_mapper=add_info_from_splitter)
                self.append_to_parallelizer_list(parallelizer_cc)
                parallelizer_rr = make_parallelizer_round_robin(mapper_spec=mapper_spec,
                                                                 aggregator_spec=aggregator_spec,
                                                                 info_splitter_mapper=add_info_from_splitter)
                self.append_to_parallelizer_list(parallelizer_rr)
