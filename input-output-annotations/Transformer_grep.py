from Meta import Meta
from ArgKindEnum import ArgKindEnum
from meta_transformer import MetaGeneratorInterface


class MetaGeneratorGrep(MetaGeneratorInterface):
    # determines the initial meta, the function for args transformations, and a function to change meta due to operands
    # [Arg] -> Meta
    #        x Arg -> (Meta -> Meta)
    #        x [Arg] -> ([Operand] x Meta) -> Meta
    def select_subcommand(arg_list):
        initial_meta = Meta([], [], None)
        transformer_for_operands = __class__.generate_operand_meta_func(arg_list)
        return (initial_meta, __class__.transformers_for_args_grep, transformer_for_operands)

    def generate_operand_meta_func(arg_list):
        if any([arg.get_name() in ["-e", "-f"] for arg in arg_list]):
            operand_slicing_parameter = 0
        else:
            operand_slicing_parameter = 1

        func = lambda operand_list, meta: meta.add_to_input_list(operand_list[operand_slicing_parameter:])
        return func

        

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

    ## Updates meta in place
    def transformers_for_args_grep(arg, meta):
        if arg.kind == ArgKindEnum.OPTION and arg.option_name == "-f":
            meta.prepend_to_input_list(arg.option_arg)