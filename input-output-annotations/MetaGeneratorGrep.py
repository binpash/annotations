
from ArgKindEnum import ArgKindEnum
from MetaGeneratorInterface import MetaGeneratorInterface


class MetaGeneratorGrep(MetaGeneratorInterface):
    # for details on what the functions do, check comments in MetaGeneratorInterface

    def transformer_for_operands(self, operand_list):
        if any([arg.get_name() in ["-e", "-f"] for arg in self.arg_list]):
            operand_slicing_parameter = 0
        else:
            operand_slicing_parameter = 1
        operand_list_strings = [operand.name for operand in operand_list]
        self.meta.add_list_to_input_list(operand_list_strings[operand_slicing_parameter:])

    # list_of_all_flags = ["-V", "--help", "-E", "-F", "-G", "-P", "-i", "--no-ignore-case", "-v", "-w",
    #                      "-x", "-y", "-c", "-L", "-l", "-o", "-q", "-s", "-b", "-H", "-h", "-n", "-T", "-Z",
    #                      "--no-group-separator", "-a", "-I", "-r", "-R", "--line-buffered", "-U", "-z"]
    # list_of_all_options = ["-e", "-f", "--color", "-m", "--label", "-A", "-B", "-C", "--group-separator",
    #                        "--binary-files", "-D", "-d", "--exclude", "--exclude-from", "--exclude-dir", "--include"]

    # Which ones do affect input/output?
    # -f affects input
    # -r actually does not really affect both since files and directories are both identified by their name
    # for now, we ignore --exclude, --exclude-from, --exclude-dir, and --include and, thus, over-approximate
    # for now, we ignore -D/-d with actions

    def transformer_for_args(self, arg):
        if arg.kind == ArgKindEnum.OPTION and arg.option_name == "-f":
            self.meta.prepend_el_to_input_list(arg.option_arg)
