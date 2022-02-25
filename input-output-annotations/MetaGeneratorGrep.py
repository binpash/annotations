from Meta import Meta
from ArgKindEnum import ArgKindEnum
from MetaGeneratorInterface import MetaGeneratorInterface


class MetaGeneratorGrep(MetaGeneratorInterface):

    # This is the select_subcommand from the original proposal,
    #   instead of returning functions, it initializes the object
    #   and then we can call its methods.
    def __init__(self, arg_list: list):
        MetaGeneratorInterface.__init__(self)
        self.arg_list = arg_list

    # Roughly corresponds to this type, but in place change of meta
    #   ([Operand] x Meta) -> Meta
    def transformer_for_operands(self, operand_list):
        if any([arg.get_name() in ["-e", "-f"] for arg in self.arg_list]):
            operand_slicing_parameter = 0
        else:
            operand_slicing_parameter = 1
        operand_list_strings = [operand.name for operand in operand_list]
        self.meta.add_to_input_list(operand_list_strings[operand_slicing_parameter:])

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

    # Roughly corresponds to this type but updates meta in place
    #   Arg -> (Meta -> Meta)
    def transformer_for_args(self, arg):
        if arg.kind == ArgKindEnum.OPTION and arg.option_name == "-f":
            self.meta.prepend_to_input_list(arg.option_arg)
