from typing import List

from util_flag_option import make_arg_simple
from datatypes_new.BasicDatatypes import FlagOption, Operand
from datatypes_new.BasicDatatypesWithIO import \
    make_stdout_with_access_output, make_stdin_with_access_stream_input
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.Splitter import make_splitter_round_robin, \
    make_splitter_indiv_files
from annotation_generation_new.datatypes.parallelizability.MapperSpec import make_mapper_spec_seq
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec, \
    make_aggregator_spec_concatenate

import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "cut"

# commands taken from spell script in one-liners


def test_cut_1() -> None:
    args: List[FlagOption] = []
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

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    goal_mapper_spec = make_mapper_spec_seq()
    goal_aggregator_spec: AggregatorSpec = make_aggregator_spec_concatenate()
    assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    assert parallelizer1.get_mapper_spec() == goal_mapper_spec
    assert parallelizer1.get_aggregator_spec() == goal_aggregator_spec
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == goal_mapper_spec
    assert parallelizer2.get_aggregator_spec() == goal_aggregator_spec


def test_cut_2() -> None:
    args = [make_arg_simple(["-z"])]
    operands = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    goal_mapper_spec = make_mapper_spec_seq()
    goal_aggregator_spec: AggregatorSpec = make_aggregator_spec_concatenate()
    assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    assert parallelizer1.get_mapper_spec() == goal_mapper_spec
    assert parallelizer1.get_aggregator_spec() == goal_aggregator_spec
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == goal_mapper_spec
    assert parallelizer2.get_aggregator_spec() == goal_aggregator_spec
