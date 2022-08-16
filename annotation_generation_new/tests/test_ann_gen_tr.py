from util_flag_option import make_arg_simple
from typing import List
from datatypes_new.BasicDatatypes import FlagOption, Operand
from datatypes_new.BasicDatatypesWithIO import \
    make_stdin_with_access_stream_input, make_stdout_with_access_output
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo

from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.Splitter import make_splitter_round_robin, \
    make_splitter_consec_chunks
from annotation_generation_new.datatypes.parallelizability.MapperSpec import make_mapper_spec_seq
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_adj_lines_merge, make_aggregator_spec_concatenate, make_aggregator_spec_adj_lines_func_from_string_representation

import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "tr"

# commands taken from spell script in one-liners


def test_tr_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-s"])]
    operands: List[Operand] = [Operand("A-Za-z"), Operand(r"'\n'")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    print(para_info.parallelizer_list)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_adj_lines_func_from_string_representation("PLACEHOLDER: remove first line if empty", False)
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_adj_lines_func_from_string_representation("PLACEHOLDER: remove first line if empty", False)

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
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_concatenate()


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
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_concatenate()


def test_tr_4() -> None:
    args: List[FlagOption] = [make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand(r"'\n'")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    print(para_info)
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()


def test_tr_5() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand(r"'\n'")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
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
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_concatenate()


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
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()
