from typing import List, Optional

from pash_annotations.util_flag_option import make_arg_simple
from pash_annotations.datatypes.BasicDatatypes import FlagOption, Operand
from pash_annotations.datatypes.BasicDatatypesWithIO import \
    make_stdout_with_access_output, make_stdin_with_access_stream_input
from pash_annotations.datatypes.CommandInvocationInitial import CommandInvocationInitial
from pash_annotations.datatypes.CommandInvocationWithIO import CommandInvocationWithIO
from pash_annotations.datatypes.CommandInvocationPrefix import CommandInvocationPrefix
from pash_annotations.annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from pash_annotations.annotation_generation.datatypes.ParallelizabilityInfo import ParallelizabilityInfo
from pash_annotations.annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from pash_annotations.annotation_generation.datatypes.parallelizability.Splitter import make_splitter_round_robin, \
    make_splitter_indiv_files, make_splitter_consec_chunks
from pash_annotations.annotation_generation.datatypes.parallelizability.MapperSpec import make_mapper_spec_seq
from pash_annotations.annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorSpec, \
    make_aggregator_spec_concatenate

import pash_annotations.annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "cut"

# commands taken from spell script in one-liners


def test_cut_1() -> None:
    args: List[FlagOption] = []
    operands: List[Operand] = [Operand("in1.txt"),
                Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: Optional[InputOutputInfo] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: Optional[ParallelizabilityInfo] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    goal_mapper_spec = make_mapper_spec_seq()
    goal_aggregator_spec: AggregatorSpec = make_aggregator_spec_concatenate()
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
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
    io_info: Optional[InputOutputInfo] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: Optional[ParallelizabilityInfo] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    goal_mapper_spec = make_mapper_spec_seq()
    goal_aggregator_spec: AggregatorSpec = make_aggregator_spec_concatenate()
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == goal_mapper_spec
    assert parallelizer1.get_aggregator_spec() == goal_aggregator_spec
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == goal_mapper_spec
    assert parallelizer2.get_aggregator_spec() == goal_aggregator_spec
