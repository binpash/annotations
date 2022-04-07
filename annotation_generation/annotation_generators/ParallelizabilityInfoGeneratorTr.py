from annotation_generation.annotation_generators.ParallelizabilityInfoGenerator_Interface import ParallelizabilityInfoGeneratorInterface
from datatypes.Operand import Operand


class ParallelizabilityInfoGeneratorTr(ParallelizabilityInfoGeneratorInterface):

    # list_of_all_flags = ["-c", "-d", "-s", "-t", "--help", "--version",
    # list_of_all_options = []

    # Which ones do affect parallelizability?
    # -d which deletes (instead of translating)
    #    -> if '\n' is effectively included in SET1, then Mp[ADJ] and Ag[ADJ]
    # -s which squeezes repetitions of characters in last spec. set
    #    -> if '\n' is effectively included in SET1, then Mp[ADJ] and Ag[ADJ]
    # for both, if nothing is true, standard things work

    def generate_info(self) -> None:
        # TODO: assert somewhere that only one set is given with -d -> should go in minimizer
        # tr does only take input from stdin, so we can always apply RR parallelizer (but Mp and Ag may change slightly)
        # check for deletion of newlines
        does_delete_newlines: bool = self.does_flag_option_list_contains_at_least_one_of(["-d"]) and \
                               self.does_last_set_effectively_contain_newline()  # only allowed to have a single set
        # check for squeezing newlines
        does_squeeze_newlines: bool = self.does_flag_option_list_contains_at_least_one_of(["-s"]) and \
                                self.does_last_set_effectively_contain_newline()
        if does_delete_newlines or does_squeeze_newlines:
            # for RR, we need an adjacent aggregator
            self.append_to_parallelizer_list_rr_seq_adjm()
            # TO CHECK: at the end, it should be a single line; this should work if we fold over results
        else:
            # for RR, we can just use concatenation
            self.append_to_parallelizer_list_rr_seq_conc()

    def does_last_set_effectively_contain_newline(self) -> bool:
        last_operand: Operand = self.operand_list[-1]
        # is contained if (a) no -c and in set, or (b) -c and not in set
        last_operand_contains_newline: bool = last_operand.contains("\n")
        if len(self.operand_list) == 1 and self.does_flag_option_list_contains_at_least_one_of(["-c"]):
            return not last_operand_contains_newline
        else:  # '-c' (if existent) does not refer to the given set
            return last_operand_contains_newline

