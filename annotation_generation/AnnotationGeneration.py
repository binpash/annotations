# imports for typing
from __future__ import annotations
from typing import overload, Literal
from datatypes.CommandInvocation import CommandInvocation
from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

# import the generator modules for input output info and parallelizability info
from config.definitions import inputoutput_info_generator_file_module_names, parallelizability_info_generator_file_and_module_names

for FILENAME_MODULE_PAIR in inputoutput_info_generator_file_module_names + parallelizability_info_generator_file_and_module_names:
    FILENAME, MODULE = FILENAME_MODULE_PAIR
    import_str = "from " + FILENAME + " import " + MODULE
    exec(import_str)

# import mappings for commands
from config.definitions import dict_cmd_name_inputoutput_info_generator_module
from config.definitions import dict_cmd_name_parallelizability_info_generator_module

# cannot be merged due to types
def get_input_output_info_from_cmd_invocation(cmd_invocation : CommandInvocation) -> InputOutputInfo:
    # Get the Generator
    info_generator_class_for_cmd = dict_cmd_name_inputoutput_info_generator_module[cmd_invocation.cmd_name]
    # Initialize the info generator object
    info_generator_object = info_generator_class_for_cmd(cmd_invocation.flag_option_list, cmd_invocation.operand_list)
    # Generate info
    info_generator_object.generate()
    return info_generator_object.get_ioinfo()

def get_parallelizability_info_from_cmd_invocation(cmd_invocation : CommandInvocation) -> ParallelizabilityInfo:
    # Get the Generator
    info_generator_class_for_cmd = dict_cmd_name_parallelizability_info_generator_module[cmd_invocation.cmd_name]
    # Initialize the info generator object
    info_generator_object = info_generator_class_for_cmd(cmd_invocation.flag_option_list, cmd_invocation.operand_list)
    # Generate info
    info_generator_object.generate()
    return info_generator_object.get_ioinfo()
