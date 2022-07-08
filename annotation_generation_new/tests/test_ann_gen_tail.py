from util_flag_option import make_arg_simple
from typing import List
from datatypes_new.BasicDatatypes import FlagOption, Operand
from datatypes_new.BasicDatatypesWithIO import make_stdout_with_access_output
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer, \
    make_parallelizer_indiv_files
from annotation_generation_new.datatypes.parallelizability.Splitter import make_splitter_indiv_files
from annotation_generation_new.datatypes.parallelizability.MapperSpec import make_mapper_spec_seq
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import make_aggregator_spec_concatenate

import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "tail"


def test_tail_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-q"])]
    operands: List[Operand] = [Operand("in1.txt"),
                               Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()
    # assert not io_info.multiple_inputs_possible # changes the result! -> different property needed ? TODO

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == make_parallelizer_indiv_files()
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()


def test_tail_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["--version"])]
    operands: List[Operand] = [Operand("in1.txt"),
                               Operand("-"),
                               Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 3
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()
    # assert not io_info.multiple_inputs_possible # changes the result! -> different property needed ? TODO

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == make_parallelizer_indiv_files()
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
