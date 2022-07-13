# imports for typing
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

# import the generator modules for input output info and parallelizability info
# from config_new.definitions import inputoutput_info_generator_file_module_names, parallelizability_info_generator_file_and_module_names
#
# for FILENAME_MODULE_PAIR in inputoutput_info_generator_file_module_names + parallelizability_info_generator_file_and_module_names:
#     FILENAME, MODULE = FILENAME_MODULE_PAIR
#     import_str = "from " + FILENAME + " import " + MODULE
#     exec(import_str)

from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorGrep import InputOutputInfoGeneratorGrep
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorMv import   InputOutputInfoGeneratorMv
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorTr import   InputOutputInfoGeneratorTr
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorCat import  InputOutputInfoGeneratorCat
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorHead import InputOutputInfoGeneratorHead
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorTail import InputOutputInfoGeneratorTail
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorCut import  InputOutputInfoGeneratorCut
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorUniq import InputOutputInfoGeneratorUniq
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorComm import InputOutputInfoGeneratorComm
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorSort import InputOutputInfoGeneratorSort
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorSed import InputOutputInfoGeneratorSed
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorCol import InputOutputInfoGeneratorCol
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorXargs import InputOutputInfoGeneratorXargs
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorExport import InputOutputInfoGeneratorExport
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorSeq import InputOutputInfoGeneratorSeq
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorTestOne import InputOutputInfoGeneratorTestOne
from annotation_generation_new.annotation_generators.InputOutputInfoGeneratorTestTwo import InputOutputInfoGeneratorTestTwo

from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorGrep import ParallelizabilityInfoGeneratorGrep
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorMv import   ParallelizabilityInfoGeneratorMv
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorTr import   ParallelizabilityInfoGeneratorTr
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorCat import  ParallelizabilityInfoGeneratorCat
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorHead import ParallelizabilityInfoGeneratorHead
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorTail import ParallelizabilityInfoGeneratorTail
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorCut import  ParallelizabilityInfoGeneratorCut
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorUniq import ParallelizabilityInfoGeneratorUniq
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorComm import ParallelizabilityInfoGeneratorComm
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorSort import ParallelizabilityInfoGeneratorSort
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorSed import ParallelizabilityInfoGeneratorSed
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorCol import ParallelizabilityInfoGeneratorCol
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorXargs import ParallelizabilityInfoGeneratorXargs
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorExport import ParallelizabilityInfoGeneratorExport
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorSeq import ParallelizabilityInfoGeneratorSeq
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorTestOne import ParallelizabilityInfoGeneratorTestOne
from annotation_generation_new.annotation_generators.ParallelizabilityInfoGeneratorTestTwo import ParallelizabilityInfoGeneratorTestTwo

# Dictionary that contains the MetaGenerator for each command
dict_cmd_name_inputoutput_info_generator_module = {
    "grep": InputOutputInfoGeneratorGrep,
    "mv":   InputOutputInfoGeneratorMv,
    "tr":   InputOutputInfoGeneratorTr,
    "cat":  InputOutputInfoGeneratorCat,
    "head": InputOutputInfoGeneratorHead,
    "tail": InputOutputInfoGeneratorTail,
    "cut":  InputOutputInfoGeneratorCut,
    "uniq": InputOutputInfoGeneratorUniq,
    "comm": InputOutputInfoGeneratorComm,
    "sort": InputOutputInfoGeneratorSort,
    "sed": InputOutputInfoGeneratorSed,
    "col": InputOutputInfoGeneratorCol,
    "xargs": InputOutputInfoGeneratorXargs,
    "export": InputOutputInfoGeneratorExport,
    "seq": InputOutputInfoGeneratorSeq,
    "test_one": InputOutputInfoGeneratorTestOne,
    "test_two": InputOutputInfoGeneratorTestTwo
}
dict_cmd_name_parallelizability_info_generator_module = {
    "grep": ParallelizabilityInfoGeneratorGrep,
    "mv":   ParallelizabilityInfoGeneratorMv,
    "tr":   ParallelizabilityInfoGeneratorTr,
    "cat":  ParallelizabilityInfoGeneratorCat,
    "head": ParallelizabilityInfoGeneratorHead,
    "tail": ParallelizabilityInfoGeneratorTail,
    "cut":  ParallelizabilityInfoGeneratorCut,
    "uniq": ParallelizabilityInfoGeneratorUniq,
    "comm": ParallelizabilityInfoGeneratorComm,
    "sort": ParallelizabilityInfoGeneratorSort,
    "sed": ParallelizabilityInfoGeneratorSed,
    "col": ParallelizabilityInfoGeneratorCol,
    "xargs": ParallelizabilityInfoGeneratorXargs,
    "export": ParallelizabilityInfoGeneratorExport,
    "seq": ParallelizabilityInfoGeneratorSeq,
    "test_one": ParallelizabilityInfoGeneratorTestOne,
    "test_two": ParallelizabilityInfoGeneratorTestTwo
}

# "mv": "Mv",
# "tr": "Tr",
# "cat": "Cat",
# "head": "Head",
# "tail": "Tail",
# "cut": "Cut",
# "uniq": "Uniq",
# "comm": "Comm"

# import mappings for commands
# from config_new.definitions import dict_cmd_name_inputoutput_info_generator_module
# from config_new.definitions import dict_cmd_name_parallelizability_info_generator_module

# cannot be merged due to types
def get_input_output_info_from_cmd_invocation(cmd_invocation : CommandInvocationInitial) -> InputOutputInfo:
    # Get the Generator
    info_generator_class_for_cmd = dict_cmd_name_inputoutput_info_generator_module[cmd_invocation.cmd_name]
    # Initialize the info generator object
    info_generator_object = info_generator_class_for_cmd(cmd_invocation)
    # Generate info
    info_generator_object.generate_info()
    return info_generator_object.get_info()

def get_parallelizability_info_from_cmd_invocation(cmd_invocation : CommandInvocationInitial) -> ParallelizabilityInfo:
    # Get the Generator
    info_generator_class_for_cmd = dict_cmd_name_parallelizability_info_generator_module[cmd_invocation.cmd_name]
    # Initialize the info generator object
    info_generator_object = info_generator_class_for_cmd(cmd_invocation)
    # Generate info
    info_generator_object.generate_info()
    return info_generator_object.get_info()
