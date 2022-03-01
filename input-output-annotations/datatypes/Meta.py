from util import *
from datatypes.FileDescriptor import *


class Meta:

    def __init__(self,
                 input_list=None,
                 output_list=None,
                 parallel_info_list=None,
                 custom_info=None):
        self.input_list = return_empty_list_if_none_else_itself(input_list)
        self.output_list = return_empty_list_if_none_else_itself(output_list)
        self.parallel_info_list = return_empty_list_if_none_else_itself(parallel_info_list)
        self.custom_info = custom_info

    def __str__(self):
        return f'meta: \n' \
            + f'\tinput_list: {self.input_list}\n' \
            + f'\toutput_list: {self.output_list}\n' \
            + f'\tcustom_info: {self.custom_info}'

    def get_input_list(self):
        return self.input_list

    def get_output_list(self):
        return self.output_list

    def add_list_to_input_list(self, input_list_to_be_added: list):
        self.input_list.extend([compute_actual_el_for_input(input_el) for input_el in input_list_to_be_added])

    def prepend_el_to_input_list(self, el_to_be_prepended):
        self.input_list.insert(0, compute_actual_el_for_input(el_to_be_prepended))

    def add_list_to_output_list(self, output_list_to_be_added: list):
        self.output_list.extend([compute_actual_el_for_output(output_el) for output_el in output_list_to_be_added])

    def prepend_el_to_output_list(self, el_to_be_prepended):
        self.output_list.insert(0, compute_actual_el_for_output(el_to_be_prepended))

    def prepend_stdin_to_input_list(self):
        # "-" is interpreted as stdin by the function
        self.input_list.insert(0, FileDescriptor.get_stdin_fd())

    def append_stdout_to_output_list(self):
        # "-" is interpreted as stdout by the function
        self.output_list.insert(-1, FileDescriptor.get_stdout_fd())

    def append_stderr_to_output_list(self):
        # "-" is interpreted as stdout by the function
        self.output_list.insert(-1, FileDescriptor.get_stderr_fd())

    def deduplicate_input_output_lists(self):
        self.input_list = list_deduplication(self.input_list)
        self.output_list = list_deduplication(self.output_list)
