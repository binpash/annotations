from util_flag_option import make_arg_simple
from typing import List, Optional
from datatypes_new.BasicDatatypes import FlagOption, FileName, Operand
from datatypes_new.BasicDatatypesWithIO import StdDescriptorWithIOInfo
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer, AdditionalInfoSplitterToMapper
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from annotation_generation_new.datatypes.parallelizability.MapperSpec import MapperSpec
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
    io_info: Optional[InputOutputInfo] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 0
    assert len(cmd_inv_with_io.get_options_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: Optional[ParallelizabilityInfo] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is None


def test_mv_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-v"])]
    operands: List[Operand] = [Operand("tomove1.txt"),
                               Operand("tomove2.txt"),
                               Operand("dest.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: Optional[InputOutputInfo] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert len(cmd_inv_with_io.get_operands_with_other_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: Optional[ParallelizabilityInfo] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is None


def test_mv_3() -> None:
    args: List[FlagOption] = [make_arg_simple(["-t", FileName("dest1.txt")]),
                              make_arg_simple(["-t", FileName("dest2.txt")])]
    # illegal to have -t twice
    operands: List[Operand] = [Operand("tomove1.txt"),
                               Operand("tomove2.txt"),
                               Operand("dest.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    io_info: Optional[InputOutputInfo] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is None
