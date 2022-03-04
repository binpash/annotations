
from datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorComm(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-1", "-2", "-3", "--check-order", "--nocheck-order", "--total", "-z", "--help", "--version"]
    # list_of_all_options = ["--output-delimiter"]

    # Which ones do affect input/output?
    # none

    def transformer_for_standard_filedescriptors(self):
        self.meta.append_stderr_to_output_list()
        self.meta.append_stdout_to_output_list()

    def transformer_for_operands(self):
        if not self.arg_list_contains_at_least_one_of(["--help", "--version"]):
            assert(len(self.operand_names_list) == 2)  # needs two files to compare
        self.meta.add_list_to_input_list(self.operand_names_list)

    def transformer_for_args(self, arg):
        pass

