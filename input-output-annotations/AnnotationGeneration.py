from metagenerators.MetaGeneratorGrep import MetaGeneratorGrep
from metagenerators.MetaGeneratorMv import MetaGeneratorMv
from metagenerators.MetaGeneratorTr import MetaGeneratorTr

# Dictionary that contains the MetaGenerator for each command
cmd_name_transformer_module_mapper = {
    "grep": MetaGeneratorGrep,
    "mv":   MetaGeneratorMv,
    "tr": MetaGeneratorTr
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

    # Get the MetaGenerator
    meta_generator_class_for_cmd = cmd_name_transformer_module_mapper[cmd_name]
    
    # Initialize the meta generator object
    meta_generator_object = meta_generator_class_for_cmd(arg_list)

    # 1) we apply the function for operands which changes meta but strip off the Operand class when passing
    meta_generator_object.transformer_for_operands([operand.name for operand in operand_list])

    # 2) we fold over the arg_list to produce the final meta
    for arg in arg_list:
        # side-effectful
        meta_generator_object.transformer_for_args(arg)

    # 3) we apply the function to determine the "std" file descriptors used
    meta_generator_object.transformer_for_standard_filedescriptors(arg_list, [operand.name for operand in operand_list])


    meta_generator_object.deduplicate_lists_of_meta()
    meta = meta_generator_object.get_meta()

    return meta

