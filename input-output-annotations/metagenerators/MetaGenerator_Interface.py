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
        # use the following functions for stdin, stdout, and stderr
        # self.meta.prepend_stdin_to_input_list()
        # self.meta.append_stdout_to_output_list()
        # self.meta.append_stderr_to_output_list()
        pass

    # Roughly corresponds to this type, but updates meta in place and list of operands is attribute
    #   ([Operand] x Meta) -> Meta
    @abstractmethod
    def transformer_for_operands(self):
        pass

    # Roughly corresponds to this type, but updates meta in place and list of operands is attribute
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
        return len(self.filter_arg_list_with(list_names)) > 0

    def filter_arg_list_with(self, list_names):
        return [arg for arg in self.arg_list if arg.get_name() in list_names]

    def if_no_file_given_add_stdin_to_input_list(self):
        if len(self.operand_names_list) == 0:
            self.meta.prepend_stdin_to_input_list()

    def deduplicate_lists_of_meta(self):
        self.meta.deduplicate_input_output_lists()

    def get_meta(self):
        return self.meta

# TODO: for most commands, --help and --version overrules the rest of the command
#  and hence we could remove the input and output lists to be more accurate,
#  we do NOT do this for now
