from annotation_generation.metagenerators.MetaGenerator_Interface import MetaGeneratorInterface
from annotation_generation.parallelizers.Parallelizer import Parallelizer
from annotation_generation.parallelizers.Aggregator import Aggregator


class MetaGeneratorUniq(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-c", "-d", "-D", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--all-repeated", "-f", "--group", "-s", "-w"]

    # Which ones do affect input/output?
    # only the number of operands and flags --help and --version

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        self.meta.append_stderr_to_output_list()
        # we add stdout and stdin in transformer_for_operands

    def apply_operands_transformer_for_input_output_lists(self):
        # tested this with the command, man-page a bit inconclusive with optional OUTPUT
        if len(self.operand_names_list) == 0:
            self.meta.prepend_stdin_to_input_list()
            self.meta.append_stdout_to_output_list()
        elif len(self.operand_names_list) == 1:
            self.meta.add_list_to_input_list(self.operand_names_list)
            self.meta.append_stdout_to_output_list()
        elif len(self.operand_names_list) == 2:
            self.meta.add_list_to_input_list(self.operand_names_list[:-1])
            self.meta.add_list_to_output_list(self.operand_names_list[-1:])
        else:
            pass    # only stderr with "uniq: extra operand '...'"

    def apply_indiv_arg_transformer_for_input_output_lists(self, arg):
        if arg.get_name() in ["--help", "--version"]:
            self.meta.append_stdout_to_output_list()

    # Which ones do affect parallelizability?
    # base-line: parallelization possible with RR/(CJ) x SEQ x ADJF
    # by using the sequential command for ADJF, we handle a lot of cases where flags contain semantic information
    # -d, -D and --all-repeated renders parallelization infeasible (at least very hard)
    # -c makes it harder but feasible:
    #   one needs to cut the prefix of numbers, run the sequential and see whether it is merged
    # TODO: what does --group do?

    def apply_transformers_for_parallelizers(self):
        # check for flags/options that make it super hard
        if not self.arg_list_contains_at_least_one_of(["-d", "-D", "--all-repeated"]):
            if self.arg_list_contains_at_least_one_of(["-c"]):
                # we need a special merge
                aggregator = Aggregator.make_aggregator_adj_lines_func("merge_count")
                parallelizer_rr_seq_adjf = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
                self.meta.append_to_parallelizer_list(parallelizer_rr_seq_adjf)
            else:
                aggregator = Aggregator.make_aggregator_adj_lines_func("seq")
                parallelizer_rr_seq_adjf = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
                self.meta.append_to_parallelizer_list(parallelizer_rr_seq_adjf)




