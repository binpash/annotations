
from datatypes.FileDescriptor import FileDescriptor, FileDescriptorEnum
from metagenerators.MetaGenerator_Interface import MetaGeneratorInterface


class MetaGeneratorUniq(MetaGeneratorInterface):
    # for details on what the functions do, check comments in its super class MetaGeneratorInterface

    # list_of_all_flags = ["-c", "-d", "-D", "-i", "-u", "-z", "--help", "--version"]
    # list_of_all_options = ["--all-repeated", "-f", "--group", "-s", "-w"]

    # Which ones do affect input/output?
    # only the number of operands and flags --help --version

    def transformer_for_standard_filedescriptors(self):
        self.meta.append_stderr_to_output_list()
        # we add stdout and stdin in transformer_for_operands

    def transformer_for_operands(self):
        # tested this with the command, man-page a bit inconclusive with optional OUTPUT
        if len(self.operand_names_list) == 0:
            self.meta.prepend_stdin_to_input_list()
            self.meta.append_stdout_to_output_list()
        elif len(self.operand_names_list) == 1:
            self.meta.append_stdout_to_output_list()
        else:
            self.meta.add_list_to_input_list(self.operand_names_list[:-1])
            self.meta.add_list_to_output_list(self.operand_names_list[-1:])

    def transformer_for_args(self, arg):
        if arg.get_name() == "--help" or arg.get_name() == "--version":
            self.meta.append_stdout_to_output_list()

