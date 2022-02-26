from datatypes.Meta import *
from abc import ABC, abstractmethod


class MetaGeneratorInterface(ABC):

    # This is the select_subcommand from the original proposal,
    #   instead of returning functions, it initializes the object
    #   and then we can call its methods.
    def __init__(self, arg_list):
        self.meta = Meta()
        self.arg_list = arg_list

    # is used to determine behaviour regarding stdin and stdout and puts them in input/output lists
    @abstractmethod
    def transformer_for_standard_filedescriptors(self, arg_list, operand_list_filenames):
        # use the following functions for stdin and stdout,
        # prepending and appending matches the intuition that stdin is the first read and stdout the last written
        # self.meta.prepend_stdin_to_input_list()
        # self.meta.append_stdout_to_output_list()
        pass

    # Roughly corresponds to this type, but updates meta in place
    #   ([Operand] x Meta) -> Meta
    @abstractmethod
    def transformer_for_operands(self, operand_list_filenames):
        pass

    # Roughly corresponds to this type, but updates meta in place
    #   Arg -> (Meta -> Meta)
    @abstractmethod
    def transformer_for_args(self, arg):
        pass

    def deduplicate_lists_of_meta(self):
        self.meta.deduplicate_input_output_lists()

    def get_meta(self):
        return self.meta

