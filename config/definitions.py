import os
import sys

### directory paths
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
ANNOTATION_GENERATORS = "annotation_generation.annotation_generators"

### macros for naming of modules

# PARALLELIZABILITY_INFO_GENERATOR_PREFIX = "ParallelizabilityInfoGenerator"
#
# # dictionary that contains the InputOutputInfoGenerator for each command
# DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {
#     "grep": "Grep",
#     "mv":   "Mv",
#     "tr": "Tr",
#     "cat": "Cat",
#     "head": "Head",
#     "tail": "Tail",
#     "cut": "Cut",
#     "uniq": "Uniq",
#     "comm": "Comm"
# }
#
# # helper function
# def str_to_class(classname):
#     return getattr(sys.modules[__name__], classname)
#
# INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX = "InputOutputInfoGenerator"
# inputoutput_info_generator_prefix_abs = ANNOTATION_GENERATORS + '.' + INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX
# # to import
# inputoutput_info_generator_file_module_names = [(inputoutput_info_generator_prefix_abs + name, INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX + name)
#                                                 for name in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values()]
# dict_cmd_name_inputoutput_info_generator_module = dict([(cmd_name, str_to_class(INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX + cmd_repr))
#                                                  for cmd_name, cmd_repr in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.items()])
#
# PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX = "ParallelizabilityInfoGenerator"
# parallelizability_info_generator_prefix_abs = ANNOTATION_GENERATORS + '.' + PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX
# # to import
# parallelizability_info_generator_file_and_module_names = [(parallelizability_info_generator_prefix_abs + name, PARALLELIZABILITY_INFO_GENERATOR_PREFIX + name)
#                                                           for name in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values()]
# dict_cmd_name_parallelizability_info_generator_module = dict([(cmd_name, str_to_class(PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX + cmd_repr))
#                                                  for cmd_name, cmd_repr in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.items()])
#
