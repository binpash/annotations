from pash_annotations.util_flag_option import make_arg_simple
from typing import List, Optional
from pash_annotations.datatypes.basic_datatypes import FlagOption, Operand
from pash_annotations.datatypes.basic_datatypes_with_io import (
    make_stdout_with_access_output,
)
from pash_annotations.datatypes.command_invocation_initial import (
    CommandInvocationInitial,
)
from pash_annotations.datatypes.command_invocation_with_io import (
    CommandInvocationWithIO,
)
from pash_annotations.datatypes.command_invocation_prefix import CommandInvocationPrefix
from pash_annotations.annotation_generation.datatypes.input_output_info import (
    InputOutputInfo,
)
from pash_annotations.annotation_generation.datatypes.parallelizability_info import (
    ParallelizabilityInfo,
)

from pash_annotations.annotation_generation.annotation_generation import AnnotationGenerator

cmd_name = "tail"


def test_tail_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-q"])]
    operands: List[Operand] = [Operand("in1.txt"), Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(
        cmd_inv.cmd_name, cmd_inv.flag_option_list, []
    )

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGenerator().get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_output
        == make_stdout_with_access_output()
    )
    # assert not io_info.multiple_inputs_possible # changes the result! -> different property needed ? TODO

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGenerator().get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is None


def test_tail_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["--version"])]
    operands: List[Operand] = [Operand("in1.txt"), Operand("-"), Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(
        cmd_inv.cmd_name, cmd_inv.flag_option_list, []
    )

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGenerator().get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 3
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_output
        == make_stdout_with_access_output()
    )
    # assert not io_info.multiple_inputs_possible # changes the result! -> different property needed ? TODO

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGenerator().get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is None
