from typing import List, Optional

from pash_annotations.util_flag_option import make_arg_simple
from pash_annotations.datatypes.basic_datatypes import FlagOption, Operand
from pash_annotations.datatypes.basic_datatypes_with_io import (
    make_stdin_with_access_stream_input,
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
    make_aggregator_spec_adj_lines_merge,
    make_aggregator_spec_concatenate,
    make_aggregator_spec_adj_lines_func_from_string_representation,
)

import pash_annotations.annotation_generation.annotation_generation as AnnotationGeneration

cmd_name = "tr"

# commands taken from spell script in one-liners


def test_tr_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-s"])]
    operands: List[Operand] = [Operand("A-Za-z"), Operand(r"'\n'")]
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
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_input
        == make_stdin_with_access_stream_input()
    )
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
    assert (
        parallelizer1.get_aggregator_spec()
        == make_aggregator_spec_adj_lines_func_from_string_representation(
            "PLACEHOLDER: remove first line if empty", False
        )
    )
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert (
        parallelizer2.get_aggregator_spec()
        == make_aggregator_spec_adj_lines_func_from_string_representation(
            "PLACEHOLDER: remove first line if empty", False
        )
    )


def test_tr_2() -> None:
    args: List[FlagOption] = []
    operands: List[Operand] = [Operand("A-Z"), Operand("a-z")]
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
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 2
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_input
        == make_stdin_with_access_stream_input()
    )
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


def test_tr_3() -> None:
    args: List[FlagOption] = [make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand("'[:punct:]'")]
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
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_input
        == make_stdin_with_access_stream_input()
    )
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


def test_tr_4() -> None:
    args: List[FlagOption] = [make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand(r"'\n'")]
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
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_input
        == make_stdin_with_access_stream_input()
    )
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
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()


def test_tr_5() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand(r"'\n'")]
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
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_input
        == make_stdin_with_access_stream_input()
    )
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


def test_tr_6() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"]), make_arg_simple(["-d"])]
    operands: List[Operand] = [Operand("A-Z")]
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
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_input
        == make_stdin_with_access_stream_input()
    )
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
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_adj_lines_merge()
