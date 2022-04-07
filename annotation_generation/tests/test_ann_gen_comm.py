from util_flag_option import make_arg_simple
from datatypes.BasicDatatypes import Operand
from datatypes.CommandInvocation import CommandInvocation
from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "comm"


def test_comm_1() -> None:
    args = [make_arg_simple(["-1"]), make_arg_simple(["-2"])]
    operands = [Operand("tocomm1.txt"),
                Operand("tocomm2.txt")]

    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 2
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert not io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0


def test_comm_2() -> None:
    args = []
    # illegal to have more than 2 files to compare
    operands = [Operand("tocomm1.txt"),
                Operand("tocomm2.txt"),
                Operand("tocomm3.txt")]
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)

    try:
        _io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
        assert False
    except Exception:
        assert True
