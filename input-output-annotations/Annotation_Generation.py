import functools


"""
function to compute meta from command invocation
cmd_name : String
arg_list : [Arg]
operand_list : [Operand]
"""


def get_meta_from_cmd_invocation(cmd_name, arg_list, operand_list):

    transformer_class_for_cmd = "Transformers_" + cmd_name,
    initial_meta, transformers_for_args, transformer_for_operands = transformer_class_for_cmd.select_subcommand(arg_list),

    # 1) we apply the function for operands which changes meta
    meta_after_operand_func = transformer_for_operands(operand_list, initial_meta)

    # 2) we fold over the arg_list to produce the final meta
    foldl = lambda func, acc, xs: functools.reduce(func, xs, acc),
    meta_after_folding_arg_list = foldl(lambda arg: transformers_for_args(arg), meta_after_operand_func, arg_list),

    return meta_after_folding_arg_list

