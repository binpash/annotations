from annotation_generation.annotation_generators.MetaGenerator_Interface import MetaGeneratorInterface
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator


class MetaGeneratorTr(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-c", "-d", "-s", "-t", "--help", "--version",
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout and no way to suppress output

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self) -> None:
        self.meta.prepend_stdin_to_input_list()
        self.meta.append_stdout_to_output_list()
        self.meta.append_stderr_to_output_list()

    # Which ones do affect parallelizability?
    # -d which deletes (instead of translating)
    #    -> if '\n' is effectively included in SET1, then Mp[ADJ] and Ag[ADJ]
    # -s which squeezes repetitions of characters in last spec. set
    #    -> if '\n' is effectively included in SET1, then Mp[ADJ] and Ag[ADJ]
    # for both, if nothing is true, standard things work

    def apply_transformers_for_parallelizers(self) -> None:
        # tr does only take input from stdin, so we can always apply RR parallelizer (but Mp and Ag may change slightly)
        # check for deletion of newlines
        does_delete_newlines = self.does_flag_option_list_contains_at_least_one_of(["-d"]) and \
                               self.does_last_set_effectively_contain_newline()  # only allowed to have a single set
        # TODO: assert somewhere that only one set is given with -d
        # check for squeezing newlines
        does_squeeze_newlines = self.does_flag_option_list_contains_at_least_one_of(["-s"]) and \
                                self.does_last_set_effectively_contain_newline()
        if does_delete_newlines or does_squeeze_newlines:
            # for RR, we need an adjacent aggregator
            # TODO: change seq to something reasonable
            aggregator = Aggregator.make_aggregator_adj_lines_merge()
            parallelizer_rr_seq_adjm = Parallelizer.make_parallelizer_round_robin(aggregator=aggregator)
            self.meta.append_to_parallelizer_list(parallelizer_rr_seq_adjm)
        else:
            # for RR, we can just use concatenation
            # TODO: change seq to something reasonable
            parallelizer_rr_seq_conc = Parallelizer.make_parallelizer_round_robin()
            self.meta.append_to_parallelizer_list(parallelizer_rr_seq_conc)

    def does_last_set_effectively_contain_newline(self) -> bool:
        last_operand = self.operand_names_list[len(self.operand_names_list) - 1]
        # is contained if (a) no -c and in set, or (b) -c and not in set
        if len(self.operand_names_list) == 1 and self.does_flag_option_list_contains_at_least_one_of(["-c"]):
            return not last_operand.__contains__("\n")
        else:  # '-c' does not refer to the given set
            return last_operand.__contains__("\n")


