from __future__ import annotations
from util import standard_repr
from annotation_generation.util import compute_actual_el_for_input, compute_actual_el_for_output
from typing import List, Optional
from datatypes.BasicDatatypes import OptionArgPosConfigType, Operand, FileDescriptor

from annotation_generation.util import return_empty_list_if_none_else_itself

class InputOutputInfo:

    def __init__(self,
                 positional_config_list : Optional[List[OptionArgPosConfigType]] = None,  # None translates to empty list
                 positional_input_list : Optional[List[FileDescriptor]] = None,  # None translates to empty list
                 positional_output_list : Optional[List[FileDescriptor]] = None,  # None translates to empty list
                 implicit_use_of_stdin : bool = False,
                 implicit_use_of_stdout : bool = False,
                 multiple_inputs_possible : bool = False
                 ) -> None:
        self.positional_config_list: List[OptionArgPosConfigType] = return_empty_list_if_none_else_itself(positional_config_list)
        # ASSUMPTION: inputs are either std* descriptors or file names, and we convert Operand into those in the setter function
        self.positional_input_list: List[FileDescriptor] = return_empty_list_if_none_else_itself(positional_input_list)
        # ASSUMPTION: outputs are either std* descriptors or file names, and we convert Operand into those in the setter function
        self.positional_output_list: List[FileDescriptor] = return_empty_list_if_none_else_itself(positional_output_list)
        self.implicit_use_of_stdin : bool = implicit_use_of_stdin
        self.implicit_use_of_stdout : bool = implicit_use_of_stdout
        self.multiple_inputs_possible : bool = multiple_inputs_possible
        # TODO: add reasonability checks somewhere -> would need getter-functions for this
        #       e.g. implicit use of stdin only when positional input list is empty

    def __repr__(self) -> str:
        return standard_repr(self)

    ### SETTER functions which convert certain types, e.g. from Operand to FileDescriptor

    def set_positional_config_list(self, some_list: List[OptionArgPosConfigType]) -> None:
        self.positional_config_list = some_list

    def set_positional_input_list(self, some_list: List[Operand]) -> None:
        some_list_hyphen_expanded: List[FileDescriptor] = [compute_actual_el_for_input(el) for el in some_list]
        self.positional_input_list = some_list_hyphen_expanded

    def set_positional_output_list(self, some_list: List[Operand]) -> None:
        some_list_hyphen_expanded: List[FileDescriptor] = [compute_actual_el_for_output(el) for el in some_list]
        self.positional_output_list = some_list_hyphen_expanded

    def set_implicit_use_of_stdin(self, value: bool) -> None:
        self.implicit_use_of_stdin = value

    def set_implicit_use_of_stdout(self, value: bool) -> None:
        self.implicit_use_of_stdout = value

    def set_multiple_inputs_possible(self, value: bool) -> None:
        self.multiple_inputs_possible = value
