import os
import sys
from typing import Optional

from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

### directory paths
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
ANNOTATION_GENERATORS = "annotation_generation_new.annotation_generators"

DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES = {
    "grep": "Grep",
    "mv":   "Mv",
    "tr": "Tr",
    "cat": "Cat",
    "head": "Head",
    "tail": "Tail",
    "cut": "Cut",
    "uniq": "Uniq",
    "comm": "Comm",
    "sort": "Sort",
    "sed": "Sed",
    "col": "Col",
    "xargs": "Xargs",
    "seq": "Seq",
    "test_one": "TestOne",
    "test_two": "TestTwo",
    "alt_bigrams_aux": "AltBigramsAux",
    "alt_bigram_aux_reduce": "AltBigramAuxReduce",
    "mkfifo": "Mkfifo",
    "diff": "Diff",
    "rm": "Rm",
    "tee": "Tee",
    "custom_sort": "CustomSort",
    "custom_tr": "CustomTr",
    "set_diff": "SetDiff",
    "bigrams_aux": "BigramsAux",
    "bigram_aux_map": "BigramAuxMap",
    "bigram_aux_reduce": "BigramAuxReduce"
}

INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX = "InputOutputInfoGenerator"
inputoutput_info_generator_prefix_abs = ANNOTATION_GENERATORS + '.' + INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX
inputoutput_info_generator_file_module_names = \
    [(inputoutput_info_generator_prefix_abs + name, INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX + name)
            for name in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values()]

PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX = "ParallelizabilityInfoGenerator"
parallelizability_info_generator_prefix_abs = ANNOTATION_GENERATORS + '.' + PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX
parallelizability_info_generator_file_and_module_names = \
    [(parallelizability_info_generator_prefix_abs + name, PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX + name)
            for name in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values()]

for FILENAME_MODULE_PAIR in inputoutput_info_generator_file_module_names + \
                            parallelizability_info_generator_file_and_module_names:
    FILENAME, MODULE = FILENAME_MODULE_PAIR
    import_str = "from " + FILENAME + " import " + MODULE
    try:
        exec(import_str)
    except ModuleNotFoundError:
        pass # it's fine if some do not exist, we catch that later


# cannot be merged due to types
def get_input_output_info_from_cmd_invocation(cmd_invocation : CommandInvocationInitial) -> Optional[InputOutputInfo]:
    # Get the Generator, info_generator_class_for_cmd_repr, info_generator_class_for_cmd_repr
    info_generator_class_for_cmd_repr = DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.get(cmd_invocation.cmd_name)
    try:
        info_generator_class_for_cmd = str_to_class(str(INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX) + str(info_generator_class_for_cmd_repr))
        # Initialize the info generator object
        info_generator_object = info_generator_class_for_cmd(cmd_invocation)
        # Generate info
        info_generator_object.generate_info()
        return info_generator_object.get_info()
    except Exception: # module does not exist
        return None

def get_parallelizability_info_from_cmd_invocation(cmd_invocation : CommandInvocationInitial) -> Optional[ParallelizabilityInfo]:
    # Get the Generator
    info_generator_class_for_cmd_repr = str(PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX) + str(DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.get(cmd_invocation.cmd_name))
    try:
        info_generator_class_for_cmd = str_to_class(info_generator_class_for_cmd_repr)
        # Initialize the info generator object
        # TODO: be more rigorous and allow empty parallelization annotation: return ParallelizabilityInfo with [] as default
        info_generator_object = info_generator_class_for_cmd(cmd_invocation)
        # Generate info
        info_generator_object.generate_info()
        return info_generator_object.get_info()
    except Exception: # module does not exist
        return None


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
