
from datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorTr(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-c", "-d", "-s", "-t", "--help", "--version",
    # list_of_all_options = []

    # Which ones do affect input/output?
    # none, takes from stdin and prints to stdout

    def transformer_for_standard_filedescriptors(self, _arg_list, _operand_list_filenames):
        self.meta.prepend_stdin_to_input_list()
        self.meta.append_stdout_to_output_list()

    def transformer_for_operands(self, operand_list_filenames):
        pass

    def transformer_for_args(self, arg):
        pass
