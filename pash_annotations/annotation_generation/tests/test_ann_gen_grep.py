from typing import List, Optional

from pash_annotations.util_flag_option import make_arg_simple
from pash_annotations.datatypes.basic_datatypes import (
    FlagOption,
    Operand,
    FileName,
    ArgStringType,
)
from pash_annotations.datatypes.basic_datatypes_with_io import (
    make_stdout_with_access_output,
)
from pash_annotations.datatypes.command_invocation_initial import (
    CommandInvocationInitial,
)
from pash_annotations.datatypes.command_invocation_with_io import (
    CommandInvocationWithIO,
)
from pash_annotations.datatypes.command_invocation_prefix import CommandInvocationPrefix
from pash_annotations.annotation_generation.datatypes.input_output_info import (
    InputOutputInfo,
)
from pash_annotations.annotation_generation.datatypes.parallelizability_info import (
    ParallelizabilityInfo,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.parallelizer import (
    Parallelizer,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.splitter import (
    make_splitter_round_robin,
    make_splitter_consec_chunks,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.mapper_spec import (
    make_mapper_spec_seq,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.aggregator_spec import (
    make_aggregator_spec_concatenate,
)

import pash_annotations.annotation_generation.annotation_generation as AnnotationGeneration

cmd_name = "grep"


def test_grep_1() -> None:
    args: List[FlagOption] = [
        make_arg_simple(["-L"]),
        make_arg_simple(["-f", FileName("dict.txt")]),
    ]
    operands: List[Operand] = [Operand("in1.txt"), Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(
        cmd_inv.cmd_name, cmd_inv.flag_option_list, []
    )

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_output
        == make_stdout_with_access_output()
    )

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 0
    # currently not implemented and thus not added to parallelizer_list
    # parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # # check that specs for mapper and aggregator are fine
    # goal_mapper_spec = make_mapper_spec_seq()
    # assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    # assert parallelizer1.get_mapper_spec() == goal_mapper_spec
    # assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
    # goal_aggregator_spec = make_aggregator_spec_custom_2_ary_from_string_representation(
    #     cmd_inv_as_str='PLACEHOLDER:merge_keeping_longer_output',
    #     is_implemented=False)
    # assert parallelizer2.get_splitter() == make_splitter_round_robin()
    # assert parallelizer2.get_mapper_spec() == goal_mapper_spec
    # assert parallelizer2.get_aggregator_spec() == goal_aggregator_spec


def test_grep_2() -> None:
    args: List[FlagOption] = [
        make_arg_simple(["-f", FileName("dict.txt")]),
        make_arg_simple(["-e", "*"]),
        make_arg_simple(["-b"]),
    ]
    operands: List[Operand] = [Operand("in1.txt"), Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(
        cmd_inv.cmd_name, cmd_inv.flag_option_list, []
    )

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_output
        == make_stdout_with_access_output()
    )

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 0
    # currently not implemented and thus not added to parallelizer_list
    # parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # # check that specs for mapper and aggregator are fine
    # assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    # assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    # assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
    # goal_mapper_spec = make_mapper_spec_custom(
    #     spec_mapper_cmd_name='PLACEHOLDER:grep_add_byte_offset',
    #     is_implemented=False)
    # assert parallelizer2.get_splitter() == make_splitter_round_robin()
    # assert parallelizer2.info_splitter_mapper == AdditionalInfoSplitterToMapper.BYTE_OFFSET
    # assert parallelizer2.get_mapper_spec() == goal_mapper_spec
    # assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_concatenate()


def test_grep_3() -> None:
    args = [
        make_arg_simple(["-f", FileName("dict.txt")]),
        make_arg_simple(["-e", ArgStringType("*")]),
        make_arg_simple(["-f", FileName("dict2.txt")]),
    ]
    operands = [Operand("in1.txt"), Operand("-")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(
        cmd_inv.cmd_name, cmd_inv.flag_option_list, []
    )

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_output
        == make_stdout_with_access_output()
    )

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_concatenate()


def test_grep_4() -> None:
    args = [
        make_arg_simple(["-f", FileName("dict.txt")]),
        make_arg_simple(["-e", ArgStringType("*")]),
        make_arg_simple(["-f", FileName("dict2.txt")]),
        make_arg_simple(["-n"]),
        make_arg_simple(["-b"]),
    ]
    operands = [Operand("in1.txt"), Operand("in2.txt"), Operand("in3.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(
        cmd_inv.cmd_name, cmd_inv.flag_option_list, []
    )

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 3
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_output
        == make_stdout_with_access_output()
    )

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 0
    # currently not implemented and thus not added to parallelizer_list
    # parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # # check that specs for mapper and aggregator are fine
    # assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    # assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    # assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_concatenate()
    # assert parallelizer2.get_splitter() == make_splitter_round_robin()
    # mapper_spec = make_mapper_spec_custom('PLACEHOLDER:grep_add_line_number_and_byte_offset',
    #                                                  is_implemented=False)
    # assert parallelizer2.info_splitter_mapper == AdditionalInfoSplitterToMapper.LINE_NUM_AND_BYTE_OFFSET
    # assert parallelizer2.get_mapper_spec() == mapper_spec
    # assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_concatenate()


def test_grep_5() -> None:
    args = [make_arg_simple(["-q"]), make_arg_simple(["-s"])]
    operands = [Operand("*"), Operand("in1.txt"), Operand("in2.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 0


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
#     assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
#     assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()
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
