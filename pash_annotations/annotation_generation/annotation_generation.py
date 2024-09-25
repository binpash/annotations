import os
import importlib
from typing import Optional

from collections import namedtuple

from pash_annotations.datatypes.command_invocation_initial import (
    CommandInvocationInitial,
)
from pash_annotations.annotation_generation.datatypes.input_output_info import (
    InputOutputInfo,
)
from pash_annotations.annotation_generation.datatypes.parallelizability_info import (
    ParallelizabilityInfo,
)

### directory paths
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

IO_INFO_PREFIX = "input_output_info_generator"
PAR_INFO_PREFIX = "parallelizability_info_generator"

FileModulePair = namedtuple("FileModulePair", ["file", "module"])


class AnnotationGenerator:
    # cannot be merged due to types
    def get_input_output_info_from_cmd_invocation(
        self,
        cmd_invocation: CommandInvocationInitial,
    ) -> Optional[InputOutputInfo]:
        try:
            # Get the Generator, info_generator_class_for_cmd_repr, info_generator_class_for_cmd_repr
            cmd = cmd_invocation.cmd_name
            module = importlib.import_module(
                f"{ANNOTATION_GENERATORS}.{IO_INFO_PREFIX}_{cmd}"
            )
            info_gen_class = getattr(
                module, self.to_pascal_case(IO_INFO_PREFIX) + self.to_pascal_case(cmd)
            )
            # Initialize the info generator object
            info_generator_object = info_gen_class(cmd_invocation)
            # Generate info
            info_generator_object.generate_info()
            return info_generator_object.get_info()
        except:
            return None

    def get_parallelizability_info_from_cmd_invocation(
        self,
        cmd_invocation: CommandInvocationInitial,
    ) -> Optional[ParallelizabilityInfo]:
        # Get the Generator
        try:
            cmd = cmd_invocation.cmd_name
            module = importlib.import_module(
                f"{ANNOTATION_GENERATORS}.{PAR_INFO_PREFIX}_{cmd}"
            )
            print(module)
            info_gen_class = getattr(
                module, self.to_pascal_case(PAR_INFO_PREFIX) + self.to_pascal_case(cmd)
            )
            # Initialize the info generator object
            info_generator_object = info_gen_class(cmd_invocation)
            # Initialize the info generator object
            # TODO: be more rigorous and allow empty parallelization annotation: return ParallelizabilityInfo with [] as default
            # Generate info
            info_generator_object.generate_info()
            return info_generator_object.get_info()
        except:
            return None

    @staticmethod
    def to_pascal_case(string: str) -> str:
        """
        Turns a snake_case string to PascalCase
        """
        return string.replace("_", " ").title().replace(" ", "")
