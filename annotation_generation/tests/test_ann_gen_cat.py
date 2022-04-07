from util_flag_option import make_arg_simple
from typing import List
from datatypes.FlagOption import FlagOption
from datatypes.Operand import Operand
from datatypes.CommandInvocation import CommandInvocation
from datatypes.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation.datatypes.parallelizability.Mapper import Mapper
from annotation_generation.datatypes.parallelizability.MapperSpec import MapperSpec
from annotation_generation.datatypes.parallelizability.AdditionalInfoFromSplitter import AdditionalInfoFromSplitter
from annotation_generation.datatypes.parallelizability.Aggregator import Aggregator
from annotation_generation.datatypes.parallelizability.AggregatorSpec import AggregatorSpec

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "cat"

def test_cat_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
    operands: List[Operand] = [Operand("in1.txt"),
                               Operand("in2.txt")]
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 2
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0    # because of -b

def test_cat_2() -> None:
    args = []
    operands = [Operand("in1.txt"),
                Operand("-"),
                Operand("in2.txt")]
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 3
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_cat_3() -> None:
    args = [make_arg_simple(["-n"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 2
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    mapper_spec = MapperSpec.make_mapper_spec_custom(spec_mapper_cmd_name='cat_offset_n_add_input',
                                                     add_info_from_splitter=AdditionalInfoFromSplitter.LINE_NUM_OFFSET,
                                                     is_implemented=False)
    parallelizer_if_cus_conc = Parallelizer.make_parallelizer_indiv_files(mapper_spec=mapper_spec)
    parallelizer_rr_cus_conc = Parallelizer.make_parallelizer_round_robin(mapper_spec=mapper_spec)
    assert parallelizer1 == parallelizer_if_cus_conc
    assert parallelizer2 == parallelizer_rr_cus_conc
    # check that results of getting mapper and aggregator are fine
    # mapper currently undefined
    # goal_mapper = Mapper.make_mapper_from_command_invocation_prefix(cmd_inv_pref)
    # assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    # assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_cat_4() -> None:
    args = [make_arg_simple(["-n"]), make_arg_simple(["-s"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 2
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0


def test_cat_5() -> None:
    args = [make_arg_simple(["-s"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 2
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    aggregator_spec = AggregatorSpec.make_aggregator_spec_adj_lines_func(spec_agg_cmd_name='merge_2_blank_lines_to_1',
                                                                         is_implemented=False)
    parallelizer_if_seq_cus = Parallelizer.make_parallelizer_indiv_files(aggregator_spec=aggregator_spec)
    parallelizer_rr_seq_cus = Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
    assert parallelizer1 == parallelizer_if_seq_cus
    assert parallelizer2 == parallelizer_rr_seq_cus
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    # goal_aggregator =
    # aggregator currently undefined
    # assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    # assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
