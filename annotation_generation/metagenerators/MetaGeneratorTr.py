
from datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorTr(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-c", "-d", "-s", "-t", "--help", "--version",
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout and no way to suppress output

    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        self.meta.prepend_stdin_to_input_list()
        self.meta.append_stdout_to_output_list()
        self.meta.append_stderr_to_output_list()
