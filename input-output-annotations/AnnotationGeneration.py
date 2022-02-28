from metagenerators.MetaGeneratorGrep import MetaGeneratorGrep
from metagenerators.MetaGeneratorMv import MetaGeneratorMv
from metagenerators.MetaGeneratorTr import MetaGeneratorTr
from metagenerators.MetaGeneratorCat import MetaGeneratorCat
from metagenerators.MetaGeneratorHead import MetaGeneratorHead
from metagenerators.MetaGeneratorTail import MetaGeneratorTail

# Dictionary that contains the MetaGenerator for each command
cmd_name_transformer_module_mapper = {
    "grep": MetaGeneratorGrep,
    "mv":   MetaGeneratorMv,
    "tr": MetaGeneratorTr,
    "cat": MetaGeneratorCat,
    "head": MetaGeneratorHead,
    "tail": MetaGeneratorTail
}

"""
function to compute meta from command invocation
cmd_name : String
arg_list : [Arg]
operand_list : [Operand]
"""


def get_meta_from_cmd_invocation(cmd_name, arg_list, operand_list):

    # Get the MetaGenerator
    meta_generator_class_for_cmd = cmd_name_transformer_module_mapper[cmd_name]
    
    # Initialize the meta generator object
    meta_generator_object = meta_generator_class_for_cmd(arg_list, operand_list)

    # 1) we apply the function for operands which changes meta but strip off the Operand class when passing
    meta_generator_object.transformer_for_operands()

    # 2) we apply the function for arg_list to produce the final meta
    meta_generator_object.transformer_for_arg_list()

    # 3) we apply the function to determine the "std" file descriptors used
    meta_generator_object.transformer_for_standard_filedescriptors()

    meta_generator_object.deduplicate_lists_of_meta()
    meta = meta_generator_object.get_meta()

    return meta

