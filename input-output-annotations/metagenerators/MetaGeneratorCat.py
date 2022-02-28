
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorCat(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface

    # list_of_all_flags = ["-A", "-b", "-e", "-E", "--number", "-s", "t", "-T", "-u", "-v", "--help", "--version"]
    # list_of_all_options = []

    # Which ones do affect input/output?
    # basically only operands and the stdout as standard output and stderr for errors

    def transformer_for_standard_filedescriptors(self):
        self.meta.append_stdout_to_output_list()
        # errors are written to stderr and cannot be suppressed
        self.meta.append_stderr_to_output_list()
        self.if_no_file_given_add_stdin_to_input_list()

    def transformer_for_operands(self):
        # all operands are inputs
        self.meta.add_list_to_input_list(self.operand_names_list)

    def transformer_for_args(self, arg):
        pass