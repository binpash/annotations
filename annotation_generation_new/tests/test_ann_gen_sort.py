from typing import List

from util_flag_option import make_arg_simple
from datatypes_new.BasicDatatypes import FlagOption, Operand, FileName, ArgStringType
from datatypes_new.CommandInvocation import CommandInvocation
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.Splitter import Splitter
from annotation_generation_new.datatypes.parallelizability.Mapper import Mapper
from annotation_generation_new.datatypes.parallelizability.Aggregator import Aggregator
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import AggregatorSpec
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import\
    TransformerFlagOptionListFilter, TransformerFlagOptionListAdd, ChainTransformerFlagOptionList


import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "sort"

# TODO: with -m, we could do a reduction tree

def test_sort_1() -> None:
    args: List[FlagOption] = []
    operands: List[Operand] = [Operand("in1.txt"),
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
    # only check splitter and actual mappers and aggregators
    assert parallelizer1.get_splitter() == Splitter.make_splitter_indiv_files()
    assert parallelizer2.get_splitter() == Splitter.make_splitter_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_custom_2_ary(cmd_name='sort', flag_option_list=[make_arg_simple(['-m'])])
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_sort_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-b"]), make_arg_simple(["-f"])]
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
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # only check splitter and actual mappers and aggregators
    assert parallelizer1.get_splitter() == Splitter.make_splitter_indiv_files()
    assert parallelizer2.get_splitter() == Splitter.make_splitter_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    flag_option_list = [make_arg_simple(["-b"]), make_arg_simple(["-f"]), make_arg_simple(["-m"])]
    goal_aggregator = Aggregator.make_aggregator_custom_2_ary(cmd_name='sort', flag_option_list=flag_option_list)
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator

def test_sort_3() -> None:
    args: List[FlagOption] = [make_arg_simple(["-s"]),
            make_arg_simple(["-o", FileName("output.txt")])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 0
    assert len(io_info.positional_output_list) == 0
    assert io_info.implicit_use_of_stdin
    assert not io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0 # because of stable sort

def test_sort_5() -> None:
    args: List[FlagOption] = [make_arg_simple(["-m"])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 0
    assert len(io_info.positional_output_list) == 0
    assert io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0 # because of stable sort


def test_sort_4() -> None:
    args: List[FlagOption] = [make_arg_simple(["--files0-from", FileName("input.txt")])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocation = CommandInvocation(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert len(io_info.positional_config_list) == 0
    assert len(io_info.positional_input_list) == 0
    assert len(io_info.positional_output_list) == 0
    assert not io_info.implicit_use_of_stdin
    assert io_info.implicit_use_of_stdout
    assert io_info.multiple_inputs_possible

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0 # because of stable sort
