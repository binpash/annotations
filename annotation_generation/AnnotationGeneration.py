from annotation_generation.metagenerators.MetaGeneratorGrep import MetaGeneratorGrep
from annotation_generation.datatypes.Meta import Meta
from datatypes.Arg import Arg
from datatypes.Operand import Operand
from typing import List

from annotation_generation.metagenerators.MetaGeneratorMv import MetaGeneratorMv
from annotation_generation.metagenerators.MetaGeneratorTr import MetaGeneratorTr
from annotation_generation.metagenerators.MetaGeneratorCat import MetaGeneratorCat
from annotation_generation.metagenerators.MetaGeneratorHead import MetaGeneratorHead
from annotation_generation.metagenerators.MetaGeneratorTail import MetaGeneratorTail
from annotation_generation.metagenerators.MetaGeneratorCut import MetaGeneratorCut
from annotation_generation.metagenerators.MetaGeneratorUniq import MetaGeneratorUniq
from annotation_generation.metagenerators.MetaGeneratorComm import MetaGeneratorComm

# Dictionary that contains the MetaGenerator for each command
cmd_name_transformer_module_mapper = {
    "grep": MetaGeneratorGrep,
    "mv":   MetaGeneratorMv,
    "tr": MetaGeneratorTr,
    "cat": MetaGeneratorCat,
    "head": MetaGeneratorHead,
    "tail": MetaGeneratorTail,
    "cut": MetaGeneratorCut,
    "uniq": MetaGeneratorUniq,
    "comm": MetaGeneratorComm
}

"""
function to compute meta from command invocation
cmd_name : String
arg_list : [Arg]
operand_list : [Operand]
"""


def get_meta_from_cmd_invocation(cmd_name: str, arg_list: List[Arg], operand_list: List[Operand]) -> Meta:

    # Get the MetaGenerator
    meta_generator_class_for_cmd = cmd_name_transformer_module_mapper[cmd_name]
    
    # Initialize the meta generator object
    meta_generator_object = meta_generator_class_for_cmd(arg_list, operand_list)

    # Apply the transformers for input/output lists
    meta_generator_object.apply_transformers_for_input_output_lists()

    # Apply the transformers for data parallelizability information
    meta_generator_object.apply_transformers_for_parallelizers()

    meta = meta_generator_object.get_meta()

    return meta

