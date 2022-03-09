
from datatypes.Arg import ArgKindEnum
from annotation_generation.metagenerators.MetaGenerator_Interface import MetaGeneratorInterface
from annotation_generation.parallelizers.Parallelizer import Parallelizer
from annotation_generation.parallelizers.Mapper import Mapper
from annotation_generation.parallelizers.Aggregator import Aggregator


class MetaGeneratorGrep(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface

    # list_of_all_flags = ["-V", "--help", "-E", "-F", "-G", "-P", "-i", "--no-ignore-case", "-v", "-w",
    #                      "-x", "-y", "-c", "-L", "-l", "-o", "-q", "-s", "-b", "-H", "-h", "-n", "-T", "-Z",
    #                      "--no-group-separator", "-a", "-I", "-r", "-R", "--line-buffered", "-U", "-z"]
    # list_of_all_options = ["-e", "-f", "--color", "-m", "--label", "-A", "-B", "-C", "--group-separator",
    #                        "--binary-files", "-D", "-d", "--exclude", "--exclude-from", "--exclude-dir", "--include"]

    # Which ones do affect input/output?
    # -f affects input
    # -r actually does not really affect both since files and directories are both identified by their name
    # for now, we ignore --exclude, --exclude-from, --exclude-dir, and --include and, thus, over-approximate
    # for now, we ignore -D/-d with actions

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        # in general, output is written to stdout but can be suppressed
        # though, --help and --version overrules this (and no actual result returned)
        output_suppressed = self.arg_list_contains_at_least_one_of(["-q"])
        version_or_help_write_to_stdout = self.arg_list_contains_at_least_one_of(["--help"]) \
                                          or self.arg_list_contains_at_least_one_of(["--version"])
        if not output_suppressed or version_or_help_write_to_stdout:
            self.meta.append_stdout_to_output_list()
        # errors are written to stderr but can be suppressed
        errors_suppressed = self.arg_list_contains_at_least_one_of(["-s"])
        if not errors_suppressed:
            self.meta.append_stderr_to_output_list()

    def apply_operands_transformer_for_input_output_lists(self):
        if self.arg_list_contains_at_least_one_of(["-e", "-f"]):
            operand_slicing_parameter = 0
        else:
            operand_slicing_parameter = 1
        operand_list_filenames = self.operand_names_list[operand_slicing_parameter:]
        # deciding on whether there is an input to check, add to input_list
        if len(operand_list_filenames) == 0:
            if self.arg_list_contains_at_least_one_of(["-r"]):
                self.meta.add_list_to_input_list("$CWD")
            else:
                self.meta.prepend_stdin_to_input_list()
        else:
            self.meta.add_list_to_input_list(operand_list_filenames)

    def apply_indiv_arg_transformer_for_input_output_lists(self, arg):
        if arg.get_name() == "-f":
            self.meta.prepend_el_to_input_list(arg.option_arg)

    # Which ones do affect parallelizability?
    # -c, -L, -l, -b, -n;
    # by checking, -L and -l overrule -c overrule -b and -n; output of -n always precedes output of -b
    # assumption: RR not over file boundaries
    # and -A, -B, and -C but we do not parallelize within file boundaries since they require context
    # for -q, the input is not read further after some condition is met, so we do not parallelize at all
    # for -m, we only do IF

    def apply_transformers_for_parallelizers(self):
        if not self.arg_list_contains_at_least_one_of(["-q"]):
            parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
            self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
            if not self.arg_list_contains_at_least_one_of(["-A", "-B", "-C", "-m"]):
                if self.arg_list_contains_at_least_one_of(["-L", "-l"]):
                    aggregator = Aggregator.make_aggregator_custom_2_ary("merge_keeping_longer_output")
                    parallelizer_rr_seq_cus2 = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_seq_cus2)
                    # the output for both options is either empty or the filename (same for both if so)
                    # for "-l": if there was a match in one part, the filename will propagate; if not, not
                    # for "-L": if there was no match in one part, the filename will propagate; it not, not
                elif self.arg_list_contains_at_least_one_of(["-c"]):
                    aggregator = Aggregator.make_aggregator_custom_2_ary("sum_indiv_results_up")
                    parallelizer_rr_seq_cus2 = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_seq_cus2)
                elif self.arg_list_contains_at_least_one_of(["-n"]) and self.arg_list_contains_at_least_one_of(["-b"]):
                    mapper = Mapper.make_mapper_custom("add_line_number_and_byte_offset")
                    parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
                elif self.arg_list_contains_at_least_one_of(["-n"]):
                    mapper = Mapper.make_mapper_custom("add_line_number_offset")
                    parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
                elif self.arg_list_contains_at_least_one_of(["-b"]):
                    mapper = Mapper.make_mapper_custom("add_byte_offset")
                    parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper=mapper)
                    self.meta.append_to_parallelizer_list(parallelizer_rr_cus_conc)
                else:   # none of the above affecting flags
                    parallelizer_rr_seq_conc = Parallelizer.make_parallelizer_round_robin()
                    self.meta.append_to_parallelizer_list(parallelizer_rr_seq_conc)
