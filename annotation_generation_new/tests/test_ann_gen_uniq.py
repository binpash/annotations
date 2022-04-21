from util_flag_option import make_arg_simple
from typing import List
from datatypes_new.BasicDatatypes import FlagOption, Operand
from datatypes_new.CommandInvocation import CommandInvocation
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec

import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "uniq"


def test_uniq_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-D"])]
    operands: List[Operand] = [Operand("in.txt"),
                               Operand("out.txt")]

    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 1
    assert len(io_info.positional_output_list) == 1
    assert not io_info.implicit_use_of_stdin
    assert not io_info.implicit_use_of_stdout
    assert not io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0


def test_uniq_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 0
    assert len(io_info.positional_output_list) == 0
    assert io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert not io_info.multiple_inputs_possible # TODO: I guess it changes the result as it does for head and tail?

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    aggregator_spec = AggregatorSpec.make_aggregator_spec_adj_lines_func('uniq_merge_count_uniq', is_implemented=False)
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    # goal_aggregator = Aggregator.make_aggregator_concatenate()
    # aggregator not implemented
    # assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_uniq_3() -> None:
    args: List[FlagOption] = []
    operands: List[Operand] = [Operand("in.txt"),
                               Operand("out.txt")]
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 1
    assert len(io_info.positional_output_list) == 1
    assert not io_info.implicit_use_of_stdin
    assert not io_info.implicit_use_of_stdout
    assert not io_info.multiple_inputs_possible # TODO: I guess it changes the result as it does for head and tail?

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # check that specs for mapper and aggregator are fine
    aggregator_spec = AggregatorSpec.make_aggregator_spec_adj_lines_seq()
    assert parallelizer1 == Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    # aggregator not implemented
    # assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
