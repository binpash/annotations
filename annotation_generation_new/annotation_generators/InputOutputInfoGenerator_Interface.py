from typing import List, Tuple, Union, Literal, Dict

from config_new.definitions import INDICATORS_FOR_FILENAMES

from datatypes_new.BasicDatatypes import Flag, Option, WhichClassForArg
from datatypes_new.AccessKind import AccessKind, get_access_from_string
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO

from annotation_generation_new.annotation_generators.Generator_Interface import Generator_Interface

from abc import ABC, abstractmethod

from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo

from parser_new.util_parser import get_json_data


class InputOutputInfoGeneratorInterface(Generator_Interface, ABC):

    # here, we only need to specify information about operands and implicitly used resources
    # information about option arguments are provided by parsing infrastructure
    # ASSUMPTION: No implicit information should be exploited since internal implementation may change


    def __init__(self, cmd_invocation: CommandInvocationInitial) -> None:
        super().__init__(cmd_invocation=cmd_invocation)
        flagoption_list_typer: List[Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                    Tuple[Literal[WhichClassForArg.ARGSTRING], None],
                                                    Tuple[Literal[WhichClassForArg.PLAINSTRING], None]]] \
                                = self.get_flagoption_list_typer_for_specific_list()
        self.input_output_info: InputOutputInfo = InputOutputInfo(
                                                    flagoption_list_typer=flagoption_list_typer,
                                                    number_of_operands=len(cmd_invocation.operand_list)
                                                  )

    @abstractmethod
    def generate_info(self) -> None:
        pass

    def get_info(self) -> InputOutputInfo:
        return self.input_output_info

    def get_cmd_inv_with_io(self, cmd_inv: CommandInvocationInitial) -> CommandInvocationWithIO:
        return self.input_output_info.apply_input_output_info_to_command_invocation(cmd_inv)

    def get_flagoption_list_typer_for_specific_list(self) -> \
            List[Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                       Tuple[Literal[WhichClassForArg.ARGSTRING], None],
                       Tuple[Literal[WhichClassForArg.PLAINSTRING], None]]]:
        dict_option_to_class_for_arg: Dict[str, Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                      Tuple[Literal[WhichClassForArg.ARGSTRING], None]]] = self.get_dict_option_to_class_for_arg()
        flagoption_list_typer = []
        for flagoption in self.cmd_inv.flag_option_list:
            if isinstance(flagoption, Flag):
                flagoption_list_typer.append((WhichClassForArg.PLAINSTRING, None))
            elif isinstance(flagoption, Option):
                flagoption_list_typer.append(dict_option_to_class_for_arg[flagoption.get_name()])
            else:
                raise Exception("neither Flag nor Option")
        return flagoption_list_typer

    def get_dict_option_to_class_for_arg(self) -> Dict[str, Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                                  Tuple[Literal[WhichClassForArg.ARGSTRING], None]]]:
        dict_option_to_class_for_arg: Dict[str, Union[Tuple[Literal[WhichClassForArg.FILESTD], AccessKind],
                                                      Tuple[Literal[WhichClassForArg.ARGSTRING], None]]] = dict()
        json_data = get_json_data(self.cmd_inv.cmd_name)
        for option_data in json_data["option"]:
            option_name = option_data[0]
            option_arg_info = option_data[-1]
            # CA whether access info is given
            if isinstance(option_arg_info, list):
                option_arg_type: str = option_arg_info[0]
                option_arg_access_str: str = option_arg_info[1]
                access: AccessKind = get_access_from_string(option_arg_access_str)
                if option_arg_type in INDICATORS_FOR_FILENAMES:
                    # for now, we do not allow to have '-' for stdin in option arguments
                    dict_option_to_class_for_arg[option_name] = (WhichClassForArg.FILESTD, access)
                else:
                    dict_option_to_class_for_arg[option_name] = (WhichClassForArg.ARGSTRING, None)
            else:
                option_arg_type: str = option_arg_info
                assert(not option_arg_type in INDICATORS_FOR_FILENAMES) # filenames need to declare access pattern, no default
                # access: AccessKind = AccessKind.make_config_input()
                dict_option_to_class_for_arg[option_name] = (WhichClassForArg.ARGSTRING, None)
        return dict_option_to_class_for_arg

    ## Library functions

    # use default values here as counter-measure for using False as default values in constructor

    def set_implicit_use_of_stdin(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdin(value)

    def set_implicit_use_of_stdout(self, value: bool = True) -> None:
        self.input_output_info.set_implicit_use_of_stdout(value)

    def if_no_operands_given_stdin_implicitly_used(self) -> None:
        if len(self.cmd_inv.operand_list) == 0:
            self.set_implicit_use_of_stdin(True)


    # forwarded to InputOutputInfo
    # Assumption: streaming inputs are always filenames or stdin
    # Assumption: (streaming) outputs are always filenames or stdout
    def all_operands_are_streaming_inputs(self) -> None:
        self.input_output_info.all_operands_are_streaming_inputs()

    def all_operands_are_streaming_outputs(self) -> None:
        self.input_output_info.all_operands_are_streaming_outputs()

    def all_operands_are_other_inputs(self) -> None:
        self.input_output_info.all_operands_are_other_inputs()

    def all_operands_are_other_outputs(self) -> None:
        self.input_output_info.all_operands_are_other_outputs()

    def all_but_last_operand_is_streaming_input(self):
        self.input_output_info.all_but_last_operand_is_streaming_input()

    def all_but_last_operand_is_other_input(self):
        self.input_output_info.all_but_last_operand_is_other_input()

    def all_but_first_operand_is_streaming_input(self):
        self.input_output_info.all_but_first_operand_is_streaming_input()

    def all_but_first_operand_is_streaming_output(self):
        self.input_output_info.all_but_first_operand_is_streaming_output()

    def all_but_first_operand_is_other_input(self):
        self.input_output_info.all_but_first_operand_is_other_input()

    def only_last_operand_is_stream_output(self):
        self.input_output_info.only_last_operand_is_stream_output()

    def only_last_operand_is_other_output(self):
        self.input_output_info.only_last_operand_is_other_output()

    def set_all_operands_as_config_arg_type_string(self):
        self.input_output_info.set_all_operands_as_config_arg_type_string()

    def set_first_operand_as_config_arg_type_string(self):
        self.input_output_info.set_first_operand_as_config_arg_type_string()

    def set_first_operand_as_config_arg_type_filename_or_std_descriptor(self):
        self.input_output_info.set_first_operand_as_config_arg_type_filename_or_std_descriptor()

    # only used for xargs
    def set_all_operands_as_arg_string(self):
        self.input_output_info.set_all_operands_as_arg_string()
