from __future__ import annotations

from annotation_generation.datatypes.Meta import *
from datatypes.FlagOption import FlagOption
from datatypes.Operand import Operand
from typing import List


class MetaGeneratorInterface:

    # This is the select_subcommand from the original proposal,
    #   instead of returning functions, it initializes the object
    #   and then we can call its methods.
    # TODO: proper type for constructor of this super class
    def __init__(self, arg_list: List[FlagOption], operand_list: List[Operand]) -> MetaGeneratorInterface:
        self.flag_option_list = arg_list
        self.operand_names_list = [operand.name for operand in operand_list]
        self.meta = Meta()

    def generate_meta(self) -> None:
        # Apply the transformers input_output_info
        self.apply_transformers_for_input_output_info()

        # Apply the transformers to obtain parallelizer lists
        self.apply_transformers_for_parallelizers()

    # we have one "big" function for each dimension of the meta,
    # which has a default way of iterating over command invocation details but can be overwritten

    # transformer scaffolding for Input-Output-Info
    def apply_transformers_for_input_output_info(self) -> None:
        # TODO
        pass

    # transformer scaffolding for INPUT/OUTPUT-LISTS
    # def apply_transformers_for_input_output_lists(self) -> None:
    #     # 1) we apply the function for operands
    #     self.apply_operands_transformer_for_input_output_lists()
    #
    #     # 2) we apply the function for arg_list to produce the final meta
    #     self.apply_arg_list_transformer_for_input_output_lists()
    #
    #     # 3) we apply the function to determine the "std" file descriptors used
    #     self.apply_standard_filedescriptor_transformer_for_input_output_lists()
    #
    #     self.deduplicate_input_output_lists_of_meta()

    # is used to determine behaviour regarding stdin and stdout and puts them in input/output lists
    # @abstractmethod, then we do not need to have the ones with pass
    # def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
    #     # use the following functions for stdin, stdout, and stderr
    #     # self.meta.prepend_stdin_to_input_list()
    #     # self.meta.append_stdout_to_output_list()
    #     # self.meta.append_stderr_to_output_list()
    #     pass

    # Roughly corresponds to this type, but updates meta in place and list of operands is attribute
    #   ([Operand] x Meta) -> Meta
    # @abstractmethod, then we do not need to have the ones with pass
    # def apply_operands_transformer_for_input_output_lists(self) -> None:
    #     pass

    # Roughly corresponds to this type, but updates meta in place and list of operands is attribute
    #   ([Arg] x Meta) -> Meta
    # def apply_arg_list_transformer_for_input_output_lists(self) -> None:
    #     for arg in self.flag_option_list:
    #         # side-effectful
    #         self.apply_indiv_arg_transformer_for_input_output_lists(arg)

    # Roughly corresponds to this type, but updates meta in place
    #   Arg -> (Meta -> Meta)
    # @abstractmethod, then we do not need to have the ones with pass
    # def apply_indiv_arg_transformer_for_input_output_lists(self, arg: Arg) -> None:
    #     pass

    # transformer for PARALLELIZERS
    def apply_transformers_for_parallelizers(self) -> None:
        # for commands which only take input from stdin, we cannot have indiv file parallelizers,
        # and for those, round robin is superior over consecutive junks, so we omit the latter even if feasible
        pass    # keep empty list for parallelizers



#     HELPER FUNCTIONS

    def get_meta(self) -> Meta:
        return self.meta

    def does_flag_option_list_contains_at_least_one_of(self, list_names: List[str]) -> bool:
        return len(self.get_flag_option_list_filtered_with(list_names)) > 0

    def get_flag_option_list_filtered_with(self, list_names: List[str]) -> List[FlagOption]:
        return [arg for arg in self.flag_option_list if arg.get_name() in list_names]

    def if_no_file_given_add_stdin_to_input_list(self) -> None:
        if len(self.operand_names_list) == 0:
            self.meta.prepend_stdin_to_input_list()
