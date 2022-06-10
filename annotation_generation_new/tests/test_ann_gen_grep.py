from util_flag_option import make_arg_simple
from typing import List
from datatypes_new.BasicDatatypes import FlagOption, ArgStringType, Operand, FileName
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

cmd_name = "grep"


def test_grep_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-L"]), make_arg_simple(["-f", FileName("dict.txt")])]
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
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    aggregator_spec = AggregatorSpec.make_aggregator_spec_custom_2_ary('merge_keeping_longer_output',
                                                                          is_implemented=False)
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(aggregator_spec=aggregator_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    # aggregator not implemented yet
    # goal_aggregator = Aggregator.make_aggregator_concatenate()
    # assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    # assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_grep_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-f", FileName("dict.txt")]),
                              make_arg_simple(["-e", "*"]),
                              make_arg_simple(["-b"])]
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
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    mapper_spec = MapperSpec.make_mapper_spec_custom('grep_add_byte_offset',
                                                     add_info_from_splitter=AdditionalInfoSplitterToMapper.BYTE_OFFSET,
                                                     is_implemented=False)
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(mapper_spec=mapper_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    # 2nd mapper not implemented yet
    # assert parallelizer2.get_actual_mapper(cmd_inv_pref) ==
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_grep_3() -> None:
    args = [make_arg_simple(["-f", FileName("dict.txt")]),
            make_arg_simple(["-e", ArgStringType("*")]),
            make_arg_simple(["-f", FileName("dict2.txt")])]
    operands = [Operand("in1.txt"),
                Operand("-")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_grep_4() -> None:
    args = [make_arg_simple(["-f", FileName("dict.txt")]),
            make_arg_simple(["-e", ArgStringType("*")]),
            make_arg_simple(["-f", FileName("dict2.txt")]),
            make_arg_simple(["-n"]),
            make_arg_simple(["-b"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt"),
                Operand("in3.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 3
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    mapper_spec = MapperSpec.make_mapper_spec_custom('grep_add_line_number_and_byte_offset',
                                                     add_info_from_splitter=AdditionalInfoSplitterToMapper.LINE_NUM_AND_BYTE_OFFSET,
                                                     is_implemented=False)
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(mapper_spec=mapper_spec)
    # check that results of getting mapper and aggregator are fine
    goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
    assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
    # 2nd mapper not implemented yet
    # assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
    goal_aggregator = Aggregator.make_aggregator_concatenate()
    assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
    assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator


def test_grep_5() -> None:
    args = [make_arg_simple(["-q"]), make_arg_simple(["-s"])]
    operands = [Operand("*"),
                Operand("in1.txt"),
                Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0

# test case removed for now (has to do with the case analysis on what to do when no file is given)
# def test_grep_6() -> None:
#     args: List[FlagOption] = []
#     operands: List[Operand] = [Operand("*")]
#     cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
#     cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])
#
#     # IO Info
#     io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
#     cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
#     print(cmd_inv_with_io.operand_list)
#     assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
#     assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
#     assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
#     assert cmd_inv_with_io.implicit_use_of_streaming_input == StdDescriptorWithIOInfo.make_stdin_with_access_stream_input()
#     assert cmd_inv_with_io.implicit_use_of_streaming_output == StdDescriptorWithIOInfo.make_stdout_with_access_output()
#
#     # Parallelizability Info
#     para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
#     assert len(para_info.parallelizer_list) == 2
#     parallelizer1: Parallelizer = para_info.parallelizer_list[0]
#     parallelizer2: Parallelizer = para_info.parallelizer_list[1]
#     # check that specs for mapper and aggregator are fine
#     assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
#     assert parallelizer2 == Parallelizer.make_parallelizer_round_robin()
#     # check that results of getting mapper and aggregator are fine
#     goal_mapper = Mapper.make_same_as_seq_mapper_from_command_invocation_prefix(cmd_inv_pref)
#     assert parallelizer1.get_actual_mapper(cmd_inv_pref) == goal_mapper
#     assert parallelizer2.get_actual_mapper(cmd_inv_pref) == goal_mapper
#     goal_aggregator = Aggregator.make_aggregator_concatenate()
#     assert parallelizer1.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
#     assert parallelizer2.get_actual_aggregator(cmd_inv_pref) == goal_aggregator
