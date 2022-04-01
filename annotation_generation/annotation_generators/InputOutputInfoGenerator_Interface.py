from __future__ import annotations

from abc import ABC, abstractmethod

from Generator_Interface import Generator_Interface
from datatypes.CommandInvocation import CommandInvocation
from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo


class InputOutputInfoGenerator_Interface(Generator_Interface, ABC):

    def __init__(self, cmd_invocation: CommandInvocation) -> InputOutputInfoGenerator_Interface:
        Generator_Interface.__init__(cmd_invocation)
        self.input_output_info: InputOutputInfo = InputOutputInfo

    @abstractmethod
    def generate_info(self) -> None:
        pass

    def get_info(self) -> InputOutputInfo:
        return self.input_output_info


    ## HELPERS/Library functions: modifying input output info

    # TODO: check functions in MetaGeneratorInterface, adapt and move here

    def if_no_file_given_stdin_implicitly_used_as_input(self) -> None:
        # TODO
        pass
