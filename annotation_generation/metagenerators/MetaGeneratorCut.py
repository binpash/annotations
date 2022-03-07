
from datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorCut(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-n", "--complement", "-s", "-z", "--help", "--version"]
    # list_of_all_options = ["-b", "-c", "-d", "-f", "--output-delimiter", ]

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout and no way to suppress output

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        self.meta.append_stdout_to_output_list()
        self.meta.append_stderr_to_output_list()
        self.if_no_file_given_add_stdin_to_input_list()

    def apply_operands_transformer_for_input_output_lists(self):
        # all operands are inputs
        self.meta.add_list_to_input_list(self.operand_names_list)
