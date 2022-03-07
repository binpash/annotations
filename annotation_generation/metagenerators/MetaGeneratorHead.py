
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorHead(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface

    # list_of_all_flags = ["-q", "-v", "-z", "--help", "--version"]
    # list_of_all_options = ["-c", "-n"]

    # Which ones do affect input/output?
    # none

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        self.meta.append_stdout_to_output_list()
        # errors are written to stderr and cannot be suppressed
        self.meta.append_stderr_to_output_list()
        self.if_no_file_given_add_stdin_to_input_list()

    def apply_operands_transformer_for_input_output_lists(self):
        # all operands are inputs
        self.meta.add_list_to_input_list(self.operand_names_list)

    # Which ones do affect parallelizability?
    # It does not really make sense to parallelize head
