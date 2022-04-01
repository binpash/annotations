from typing import List

from annotation_generation.annotation_generators.MetaGeneratorGrep import MetaGeneratorGrep
from annotation_generation.datatypes.Meta import Meta
from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from datatypes.FlagOption import FlagOption
from datatypes.Operand import Operand
from datatypes.CommandInvocation import CommandInvocation


from annotation_generation.annotation_generators.MetaGeneratorMv import MetaGeneratorMv
from annotation_generation.annotation_generators.MetaGeneratorTr import MetaGeneratorTr
from annotation_generation.annotation_generators.MetaGeneratorCat import MetaGeneratorCat
from annotation_generation.annotation_generators.MetaGeneratorHead import MetaGeneratorHead
from annotation_generation.annotation_generators.MetaGeneratorTail import MetaGeneratorTail
from annotation_generation.annotation_generators.MetaGeneratorCut import MetaGeneratorCut
from annotation_generation.annotation_generators.MetaGeneratorUniq import MetaGeneratorUniq
from annotation_generation.annotation_generators.MetaGeneratorComm import MetaGeneratorComm

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


def get_meta_from_cmd_invocation(cmd_name: str, arg_list: List[FlagOption], operand_list: List[Operand]) -> Meta:

    # Get the MetaGenerator
    meta_generator_class_for_cmd = cmd_name_transformer_module_mapper[cmd_name]
    
    # Initialize the meta generator object
    meta_generator_object = meta_generator_class_for_cmd(arg_list, operand_list)

    # Generate meta
    meta_generator_object.generate_meta()

    meta = meta_generator_object.get_meta()

    return meta


def get_input_output_info_from_cmd_invocation(cmd_invocation : CommandInvocation) -> InputOutputInfo:
    # Get the InputOutputInfoGenerator
    ioinfo_generator_class_for_cmd = cmd_name_transformer_module_mapper[cmd_invocation.cmd_name]

    # Initialize the input-output-info generator object
    ioinfo_generator_object = ioinfo_generator_class_for_cmd(cmd_invocation.flag_option_list, cmd_invocation.operand_list)

    # Generate meta
    ioinfo_generator_object.generate()

    ioinfo = ioinfo_generator_object.get_ioinfo()

    return ioinfo

