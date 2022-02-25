from MetaGeneratorGrep import MetaGeneratorGrep
from MetaGeneratorMv import MetaGeneratorMv
from util import *

# Dictionary that contains the MetaGenerator for each command
cmd_name_transformer_module_mapper = {
    "grep": MetaGeneratorGrep,
    "mv":   MetaGeneratorMv
}

"""
function to compute meta from command invocation
cmd_name : String
arg_list : [Arg]
operand_list : [Operand]
"""


def get_meta_from_cmd_invocation(cmd_name, arg_list, operand_list):

    # TODO: Consider whether we want the Meta to be completely
    #       handled in the meta generator, or whether we want the
    #       annotation generator to have transparency.

    # Get the metagenerator
    meta_generator_class_for_cmd = cmd_name_transformer_module_mapper[cmd_name]
    
    # Initialize the meta generator object
    meta_generator_object = meta_generator_class_for_cmd(arg_list)

    # 1) we apply the function for operands which changes meta
    meta_generator_object.transformer_for_operands(operand_list)

    # 2) we fold over the arg_list to produce the final meta
    for arg in arg_list:
        # side-effectful
        meta_generator_object.transformer_for_args(arg)
    
    meta = meta_generator_object.get_deduplicated_meta()

    return meta

