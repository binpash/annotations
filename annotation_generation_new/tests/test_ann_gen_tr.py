from util_flag_option import make_arg_simple
from typing import List
from datatypes_new.BasicDatatypes import FlagOption, Operand
from datatypes_new.BasicDatatypesWithIO import StdDescriptorWithIOInfo
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec

import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "tr"

# commands taken from spell script in one-liners


def test_tr_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-s"])]
    operands: List[Operand] = [Operand("A-Za-z"), Operand("\'\n\'")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == StdDescriptorWithIOInfo.make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    aggregator_spec = AggregatorSpec.make_aggregator_spec_adj_lines_merge()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_adj_lines_merge()
    # aggregator not implemented
    # assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator

def test_tr_2() -> None:
    args: List[FlagOption] = []
    operands: List[Operand] = [Operand("A-Z"), Operand("a-z")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == StdDescriptorWithIOInfo.make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_tr_3() -> None:
    args: List[FlagOption] = [make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand("'[:punct:]'")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == StdDescriptorWithIOInfo.make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_tr_4() -> None:
    args: List[FlagOption] = [make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand("'\n'")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == StdDescriptorWithIOInfo.make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    aggregator_spec = AggregatorSpec.make_aggregator_spec_adj_lines_merge()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_adj_lines_merge()
    # aggregator not implemented
    # assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_tr_5() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand("'\n'")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == StdDescriptorWithIOInfo.make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_tr_6() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand("A-Z")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == StdDescriptorWithIOInfo.make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    aggregator_spec = AggregatorSpec.make_aggregator_spec_adj_lines_merge()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_adj_lines_merge()
    # aggregator not implemented
    # assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
