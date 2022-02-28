
from datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorCut(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter", ]

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout and no way to suppress output

    def transformer_for_standard_filedescriptors(self):
        self.meta.append_stdout_to_output_list()
        self.meta.append_stderr_to_output_list()
        self.if_no_file_given_add_stdin_to_input_list()

    def transformer_for_operands(self):
        # all operands are inputs
        self.meta.add_list_to_input_list(self.operand_names_list)

    def transformer_for_args(self, arg):
        pass
