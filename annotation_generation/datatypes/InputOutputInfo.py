from __future__ import annotations
from util import standard_repr
from typing import List, Optional
from datatypes.Operand import Operand

from annotation_generation.util import return_empty_list_if_none_else_itself

class InputOutputInfo:

    def __init__(self,
                 positional_config_list : Optional[List[Operand]] = None,  # None translates to empty list
                 positional_input_list : Optional[List[Operand]] = None,   # None translates to empty list
                 positional_output_list : Optional[List[Operand]] = None,  # None translates to empty list
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
