from datatypes.Meta import *
from abc import ABC, abstractmethod


class MetaGeneratorInterface(ABC):

    # This is the select_subcommand from the original proposal,
    #   instead of returning functions, it initializes the object
    #   and then we can call its methods.
    def __init__(self, arg_list, operand_list):
        self.meta = Meta()
        self.arg_list = arg_list
        self.operand_names_list = [operand.name for operand in operand_list]

    # we have one "big" function for each dimension of the meta, e.g. apply_transformers_for_input_output_lists
    # which has a default way of iterating over command invocation details but can be overwritten

    # transformer scaffolding for INPUT/OUTPUT-LISTS
    def apply_transformers_for_input_output_lists(self):
        # 1) we apply the function for operands
        self.apply_operands_transformer_for_input_output_lists()

        # 2) we apply the function for arg_list to produce the final meta
        self.apply_arg_list_transformer_for_input_output_lists()

        # 3) we apply the function to determine the "std" file descriptors used
        self.apply_standard_filedescriptor_transformer_for_input_output_lists()

        self.deduplicate_input_output_lists_of_meta()

    # is used to determine behaviour regarding stdin and stdout and puts them in input/output lists
    # @abstractmethod, then we do not need to have the ones with pass
    def apply_standard_filedescriptor_transformer_for_input_output_lists(self):
        # use the following functions for stdin, stdout, and stderr
        # self.meta.prepend_stdin_to_input_list()
        # self.meta.append_stdout_to_output_list()
        # self.meta.append_stderr_to_output_list()
        pass

    # Roughly corresponds to this type, but updates meta in place and list of operands is attribute
    #   ([Operand] x Meta) -> Meta
    # @abstractmethod, then we do not need to have the ones with pass
    def apply_operands_transformer_for_input_output_lists(self):
        pass

    # Roughly corresponds to this type, but updates meta in place and list of operands is attribute
    #   ([Arg] x Meta) -> Meta
    def apply_arg_list_transformer_for_input_output_lists(self):
        for arg in self.arg_list:
            # side-effectful
            self.apply_indiv_arg_transformer_for_input_output_lists(arg)

    # Roughly corresponds to this type, but updates meta in place
    #   Arg -> (Meta -> Meta)
    # @abstractmethod, then we do not need to have the ones with pass
    def apply_indiv_arg_transformer_for_input_output_lists(self, arg):
        pass

    def deduplicate_input_output_lists_of_meta(self):
        self.meta.deduplicate_input_output_lists()

    # transformer for PARALLELIZERS
    def apply_transformers_for_parallelizers(self):
        # for commands which only take input from stdin, we cannot have indiv file parallelizers,
        # and for those, round robin is superior over consecutive junks, so we omit the latter even if feasible
        pass    # keep empty list for parallelizers

#     HELPER FUNCTIONS

    def get_meta(self):
        return self.meta

    def arg_list_contains_at_least_one_of(self, list_names):
        return len(self.filter_arg_list_with(list_names)) > 0

    def filter_arg_list_with(self, list_names):
        return [arg for arg in self.arg_list if arg.get_name() in list_names]

    def if_no_file_given_add_stdin_to_input_list(self):
        if len(self.operand_names_list) == 0:
            self.meta.prepend_stdin_to_input_list()


# TODO: for most commands, --help and --version overrules the rest of the command
#  and hence we could remove the input and output lists to be more accurate,
#  we do NOT do this for now
