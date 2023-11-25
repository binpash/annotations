from typing import Optional

from pash_annotations.util_flag_option import make_arg_simple
from pash_annotations.datatypes.basic_datatypes import Operand
from pash_annotations.datatypes.basic_datatypes_with_io import (
    make_stdout_with_access_output,
)
from pash_annotations.datatypes.command_invocation_initial import (
    CommandInvocationInitial,
)
from pash_annotations.datatypes.command_invocation_with_io import (
    CommandInvocationWithIO,
)
from pash_annotations.annotation_generation.datatypes.input_output_info import (
    InputOutputInfo,
)
from pash_annotations.annotation_generation.datatypes.parallelizability_info import (
    ParallelizabilityInfo,
)
from pash_annotations.annotation_generation.annotation_generation import AnnotationGenerator

cmd_name = "comm"


def test_comm_1() -> None:
    args = [make_arg_simple(["-1"]), make_arg_simple(["-2"])]
    operands = [Operand("tocomm1.txt"), Operand("tocomm2.txt")]

    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
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

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGenerator().get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is None


def test_comm_2() -> None:
    args = []
    # illegal to have more than 2 files to compare
    operands = [Operand("tocomm1.txt"), Operand("tocomm2.txt"), Operand("tocomm3.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )

    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGenerator().get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is None
