import functools

from Transformer_grep import MetaGeneratorGrep
from util import *

## Dictionary that contains the MetaGenerator for each command
cmd_name_transformer_module_mapper = {
    "grep": MetaGeneratorGrep
}

"""
function to compute meta from command invocation
cmd_name : String
arg_list : [Arg]
operand_list : [Operand]
"""


def get_meta_from_cmd_invocation(cmd_name, arg_list, operand_list):

    transformer_class_for_cmd = cmd_name_transformer_module_mapper[cmd_name]

    meta, transformers_for_args, transformer_for_operands = transformer_class_for_cmd.select_subcommand(arg_list)

    # 1) we apply the function for operands which changes meta
    transformer_for_operands(operand_list, meta)

    # 2) we fold over the arg_list to produce the final meta
    for arg in arg_list:
        ## Side-effectful
        transformers_for_args(arg, meta)
    
    return meta

