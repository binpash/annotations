import os
import sys
from typing import Optional

from collections import namedtuple

from pash_annotations.datatypes.command_invocation_initial import (
    CommandInvocationInitial,
)
from datatypes.input_output_info import InputOutputInfo
from datatypes.parallelizability_info import ParallelizabilityInfo

### directory paths
ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), "../.."))
ANNOTATION_GENERATORS = "pash_annotations.annotation_generation.annotation_generators"
CMD_NAMES = [
    "alt_bigrams_aux",
    "alt_bigram_aux_reduce",
    "awk",
    "bigrams_aux",
    "bigram_aux_map",
    "bigram_aux_reduce",
    "cat",
    "col",
    "comm",
    "custom_sort",
    "custom_tr",
    "cut",
    "diff",
    "grep",
    "head",
    "mkfifo",
    "mv",
    "rm",
    "sed",
    "set_diff",
    "seq",
    "sort",
    "tail",
    "tee",
    "test_one",
    "test_two",
    "tr",
    "uniq",
    "xarg",
    "wc",
]


def to_pascal_case(string: str) -> str:
    """
    Turns a snake_case string to PascalCase
    """
    return string.replace("_", " ").title().replace(" ", "")


IO_INFO_PREFIX = "input_output_info_generator"
PAR_INFO_PREFIX = "parallelizability_info_generator"

FileModulePair = namedtuple("FileModulePair", ["file", "module"])

io_info_gen_file_module_names = [
    FileModulePair(
        f"{ANNOTATION_GENERATORS}.{IO_INFO_PREFIX}_{cmd}",
        to_pascal_case(IO_INFO_PREFIX) + to_pascal_case(cmd),
    )
    for cmd in CMD_NAMES
]

par_info_gen_file_module_names = [
    FileModulePair(
        f"{ANNOTATION_GENERATORS}.{PAR_INFO_PREFIX}_{cmd}",
        to_pascal_case(PAR_INFO_PREFIX) + to_pascal_case(cmd),
    )
    for cmd in CMD_NAMES
]

for filename, module in io_info_gen_file_module_names + par_info_gen_file_module_names:
    import_str = "from " + filename + " import " + module
    try:
        exec(import_str)
    except ModuleNotFoundError:
        pass  # it's fine if some do not exist, we catch that later


# cannot be merged due to types
def get_input_output_info_from_cmd_invocation(
    cmd_invocation: CommandInvocationInitial,
) -> Optional[InputOutputInfo]:
    # Get the Generator, info_generator_class_for_cmd_repr, info_generator_class_for_cmd_repr
    try:
        info_generator_class_for_cmd = str_to_class(
            to_pascal_case(IO_INFO_PREFIX) + to_pascal_case(cmd_invocation.cmd_name)
        )
        # Initialize the info generator object
        info_generator_object = info_generator_class_for_cmd(cmd_invocation)
        # Generate info
        info_generator_object.generate_info()
        return info_generator_object.get_info()
    except Exception as sth:  # module does not exist
        return None


def get_parallelizability_info_from_cmd_invocation(
    cmd_invocation: CommandInvocationInitial,
) -> Optional[ParallelizabilityInfo]:
    # Get the Generator
    try:
        info_generator_class_for_cmd = str_to_class(
            to_pascal_case(PAR_INFO_PREFIX) + to_pascal_case(cmd_invocation.cmd_name)
        )
        # Initialize the info generator object
        # TODO: be more rigorous and allow empty parallelization annotation: return ParallelizabilityInfo with [] as default
        info_generator_object = info_generator_class_for_cmd(cmd_invocation)
        # Generate info
        info_generator_object.generate_info()
        return info_generator_object.get_info()
    except Exception:  # module does not exist
        return None


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
