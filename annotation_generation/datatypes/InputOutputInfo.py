from __future__ import annotations
from util import standard_repr
from annotation_generation.util import compute_actual_el_for_input, compute_actual_el_for_output
from typing import List, Optional, Union
from datatypes.Operand import Operand
from datatypes.FileDescriptor import FileDescriptor

from annotation_generation.util import return_empty_list_if_none_else_itself

class InputOutputInfo:

    def __init__(self,
                 positional_config_list : Optional[List[Operand]] = None,  # None translates to empty list
                 positional_input_list : Optional[List[FileDescriptor]] = None,  # None translates to empty list
                 positional_output_list : Optional[List[FileDescriptor]] = None,  # None translates to empty list
                 implicit_use_of_stdin : bool = False,
                 implicit_use_of_stdout : bool = False,
                 multiple_inputs_possible : bool = False
                 ) -> InputOutputInfo:
        self.positional_config_list = return_empty_list_if_none_else_itself(positional_config_list)
        self.positional_input_list = return_empty_list_if_none_else_itself(positional_input_list)
        self.positional_output_list = return_empty_list_if_none_else_itself(positional_output_list)
        self.implicit_use_of_stdin : bool = implicit_use_of_stdin
        self.implicit_use_of_stdout : bool = implicit_use_of_stdout
        self.multiple_inputs_possible : bool = multiple_inputs_possible
        # TODO: add reasonability checks somewhere
        # TODO: make sure that types of positional_config_list determine whether something is a str or file name/descriptor

    def __repr__(self) -> str:
        return standard_repr(self)

    ### SETTER functions which convert certain types, e.g. from Operand to FileDescriptor

    def set_positional_config_list(self, some_list: List[Operand]) -> None:
        self.positional_config_list = some_list

    def set_positional_input_list(self, some_list: List[Operand]) -> None:
        some_list_hyphen_expanded = [compute_actual_el_for_input(el) for el in some_list]
        self.positional_input_list = some_list_hyphen_expanded

    def set_positional_output_list(self, some_list: List[Operand]) -> None:
        some_list_hyphen_expanded = [compute_actual_el_for_output(el) for el in some_list]
        self.positional_output_list = some_list_hyphen_expanded

    def set_implicit_use_of_stdin(self, value: bool) -> None:
        self.implicit_use_of_stdin = value

    def set_implicit_use_of_stdout(self, value: bool) -> None:
        self.implicit_use_of_stdout = value

    def set_multiple_inputs_possible(self, value: bool) -> None:
        self.multiple_inputs_possible = value


    # CANDIDATES for library functions
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
