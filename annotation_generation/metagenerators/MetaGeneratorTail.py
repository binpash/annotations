
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface
from parallelizers.Parallelizer import Parallelizer


class MetaGeneratorTail(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface
    # basically the same as for HEAD but man page for TAIL is a bit longer

    # list_of_all_flags = ["-q", "--retry", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-f", "-n", "-max-unchanged-stats", "--pid", "-s"]

    # Which ones do affect input/output?
    # none

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        self.meta.append_stdout_to_output_list()
        self.meta.append_stderr_to_output_list()  # errors are written to stderr and cannot be suppressed
        self.if_no_file_given_add_stdin_to_input_list()

    def apply_operands_transformer_for_input_output_lists(self):
        # all operands are inputs
        self.meta.add_list_to_input_list(self.operand_names_list)

    # Which ones do affect parallelizability?
    # we can parallelize individual files

    def apply_transformers_for_parallelizers(self):
        parallelizer_if_seq_conc = Parallelizer.make_parallelizer_indiv_files()
        self.meta.append_to_parallelizer_list(parallelizer_if_seq_conc)
