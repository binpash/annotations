from __future__ import annotations
from typing import List

from util import standard_repr, standard_eq
from annotation_generation.util import return_empty_list_if_none_else_itself
from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer


class Meta:

    def __init__(self,
                 input_output_info : InputOutputInfo,
                 parallelizer_list: None = None,  # None translates to empty list
                 ) -> Meta:
        self.input_output_info = input_output_info
        self.parallelizer_list = return_empty_list_if_none_else_itself(parallelizer_list)

    def __repr__(self):
        return standard_repr(self)

    def __eq__(self, other):
        return standard_eq(self, other)


    # GETTERS
    def get_input_output_info(self) -> InputOutputInfo:
        return self.input_output_info

    def get_parallelizer_list(self) -> List[Parallelizer]:
        return self.parallelizer_list

    # modifiers for input/output-lists
    # def add_list_to_input_list(self, input_list_to_be_added: list[str]) -> None:
    #     self.input_list.extend([compute_actual_el_for_input(input_el) for input_el in input_list_to_be_added])
    #
    # def prepend_el_to_input_list(self, el_to_be_prepended: str) -> None:
    #     self.input_list.insert(0, compute_actual_el_for_input(el_to_be_prepended))
    #
    # def add_list_to_output_list(self, output_list_to_be_added: list[str]) -> None:
    #     self.output_list.extend([compute_actual_el_for_output(output_el) for output_el in output_list_to_be_added])
    #
    # def prepend_el_to_output_list(self, el_to_be_prepended: str) -> None:
    #     self.output_list.insert(0, compute_actual_el_for_output(el_to_be_prepended))
    #
    # def prepend_stdin_to_input_list(self) -> None:
    #     # "-" is interpreted as stdin by the function
    #     self.input_list.insert(0, FileDescriptor.get_stdin_fd())
    #
    # def append_stdout_to_output_list(self) -> None:
    #     # "-" is interpreted as stdout by the function
    #     self.output_list.insert(-1, FileDescriptor.get_stdout_fd())
    #
    # def append_stderr_to_output_list(self) -> None:
    #     # "-" is interpreted as stdout by the function
    #     self.output_list.insert(-1, FileDescriptor.get_stderr_fd())

    # modifiers for parallelizer list

    def append_to_parallelizer_list(self, el_to_be_appended: Parallelizer) -> None:
        self.parallelizer_list.append(el_to_be_appended)
