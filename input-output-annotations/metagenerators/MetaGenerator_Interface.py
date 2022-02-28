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

    # is used to determine behaviour regarding stdin and stdout and puts them in input/output lists
    @abstractmethod
    def transformer_for_standard_filedescriptors(self):
        # use the following functions for stdin and stdout,
        # prepending and appending matches the intuition that stdin is the first read and stdout the last written
        # self.meta.prepend_stdin_to_input_list()
        # self.meta.append_stdout_to_output_list()
        pass

    # Roughly corresponds to this type, but updates meta in place
    #   ([Operand] x Meta) -> Meta
    @abstractmethod
    def transformer_for_operands(self):
        pass

    # Roughly corresponds to this type, but updates meta in place
    #   ([Arg] x Meta) -> Meta
    def transformer_for_arg_list(self):
        for arg in self.arg_list:
            # side-effectful
            self.transformer_for_args(arg)

    # Roughly corresponds to this type, but updates meta in place
    #   Arg -> (Meta -> Meta)
    @abstractmethod
    def transformer_for_args(self, arg):
        pass

    def arg_list_contains_at_least_one_of(self, list_names):
        return any([arg.get_name() in list_names for arg in self.arg_list])

    def if_no_file_given_add_stdin_to_input_list(self):
        if self.operand_names_list is []:
            self.meta.prepend_stdin_to_input_list()

    def deduplicate_lists_of_meta(self):
        self.meta.deduplicate_input_output_lists()

    def get_meta(self):
        return self.meta

