import os
import sys

### which argument strings in command_flag_option_info/data/*.json files are interpreted as filenames/directories
INDICATORS_FOR_FILENAMES = ["FILE", "DIR", "DIRECTORY"]

### directory paths
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
ANNOTATION_GENERATORS = "annotation_generation_new.annotation_generators"

### macros for naming of modules

PARALLELIZABILITY_INFO_GENERATOR_PREFIX = "ParallelizabilityInfoGenerator"

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

# helper function
def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)

INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX = "InputOutputInfoGenerator"
inputoutput_info_generator_prefix_abs = ANNOTATION_GENERATORS + '.' + INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX

def get_inputoutput_info_generator_file_module_names():
    return [(inputoutput_info_generator_prefix_abs + name, INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX + name)
                                        for name in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values()]

def get_dict_cmd_name_inputoutput_info_generator_module():
    return dict([(cmd_name, str_to_class(INPUTOUTPUT_INFO_FILENAME_MODULE_PREFIX + cmd_repr))
                                        for cmd_name, cmd_repr in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.items()])

PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX = "ParallelizabilityInfoGenerator"
parallelizability_info_generator_prefix_abs = ANNOTATION_GENERATORS + '.' + PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX
# to import
def get_parallelizability_info_generator_file_and_module_names():
    return [(parallelizability_info_generator_prefix_abs + name, PARALLELIZABILITY_INFO_GENERATOR_PREFIX + name)
                                        for name in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.values()]

def get_dict_cmd_name_parallelizability_info_generator_module():
    return dict([(cmd_name, str_to_class(PARALLELIZABILITY_INFO_FILENAME_MODULE_PREFIX + cmd_repr))
                                        for cmd_name, cmd_repr in DICT_CMD_NAME_TO_REPRESENTATION_IN_MODULE_NAMES.items()])
