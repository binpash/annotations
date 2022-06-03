from util_flag_option import make_arg_simple
from typing import List
from datatypes_new.BasicDatatypes import FlagOption, FileName, Operand
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from annotation_generation_new.datatypes.parallelizability.MapperSpec import MapperSpec
from annotation_generation_new.datatypes.parallelizability.AdditionalInfoFromSplitter import AdditionalInfoFromSplitter
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec

import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "mv"


def test_mv_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-t", FileName("dest")])]
    operands: List[Operand] = [Operand("tomove1.txt"),
                               Operand("tomove2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 2
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert not io_info.implicit_use_of_stdout
    assert not io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0


def test_mv_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-v"])]
    operands: List[Operand] = [Operand("tomove1.txt"),
                               Operand("tomove2.txt"),
                               Operand("dest.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 2
    assert len(io_info.positional_output_list) == 1
    assert not io_info.implicit_use_of_stdin
    assert not io_info.implicit_use_of_stdout
    assert not io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0


def test_mv_3() -> None:
    args: List[FlagOption] = [make_arg_simple(["-t", FileName("dest1.txt")]),
                              make_arg_simple(["-t", FileName("dest2.txt")])]
    # illegal to have -t twice
    operands: List[Operand] = [Operand("tomove1.txt"),
                               Operand("tomove2.txt"),
                               Operand("dest.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    try:
        _io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
        assert False
    except Exception:
        assert True
