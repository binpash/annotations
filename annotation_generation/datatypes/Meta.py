from __future__ import annotations

from annotation_generation.util import *
from annotation_generation.datatypes.FileDescriptor import *
from annotation_generation.datatypes.FileName import FileName
from annotation_generation.parallelizers.Parallelizer import Parallelizer
from typing import List, Union


class Meta:

    def __init__(self,
                 input_list: None=None,
                 output_list: None=None,
                 parallelizer_list: None=None,
                 custom_info: None=None) -> None:
        self.input_list = return_empty_list_if_none_else_itself(input_list)
        self.output_list = return_empty_list_if_none_else_itself(output_list)
        self.parallelizer_list = return_empty_list_if_none_else_itself(parallelizer_list)
        self.custom_info = custom_info
    #     TODO: add info whether command can take sequence of inputs (or we need cat to merge them)

    def __str__(self):
        return f'meta: \n' \
            + f'\tinput_list: {self.input_list}\n' \
            + f'\toutput_list: {self.output_list}\n' \
            + f'\tparallelizer_list: {self.parallelizer_list}\n' \
            + f'\tcustom_info: {self.custom_info}'

    # GETTERS
    def get_input_list(self) -> List[Union[FileDescriptor, FileName]]:
        return self.input_list

    def get_output_list(self) -> List[Union[FileDescriptor, FileName]]:
        return self.output_list

    def get_parallelizer_list(self) -> List[Parallelizer]:
        return self.parallelizer_list

    # modifiers for input/output-lists
    def add_list_to_input_list(self, input_list_to_be_added: list[str]) -> None:
        self.input_list.extend([compute_actual_el_for_input(input_el) for input_el in input_list_to_be_added])

    def prepend_el_to_input_list(self, el_to_be_prepended: str) -> None:
        self.input_list.insert(0, compute_actual_el_for_input(el_to_be_prepended))

    def add_list_to_output_list(self, output_list_to_be_added: list[str]) -> None:
        self.output_list.extend([compute_actual_el_for_output(output_el) for output_el in output_list_to_be_added])

    def prepend_el_to_output_list(self, el_to_be_prepended: str) -> None:
        self.output_list.insert(0, compute_actual_el_for_output(el_to_be_prepended))

    def prepend_stdin_to_input_list(self) -> None:
        # "-" is interpreted as stdin by the function
        self.input_list.insert(0, FileDescriptor.get_stdin_fd())

    def append_stdout_to_output_list(self) -> None:
        # "-" is interpreted as stdout by the function
        self.output_list.insert(-1, FileDescriptor.get_stdout_fd())

    def append_stderr_to_output_list(self) -> None:
        # "-" is interpreted as stdout by the function
        self.output_list.insert(-1, FileDescriptor.get_stderr_fd())

    def deduplicate_input_output_lists(self) -> None:
        self.input_list = list_deduplication(self.input_list)
        self.output_list = list_deduplication(self.output_list)

    # modifiers for parallelizer list

    def append_to_parallelizer_list(self, el_to_be_appended: Parallelizer) -> None:
        self.parallelizer_list.append(el_to_be_appended)
