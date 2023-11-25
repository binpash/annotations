from typing import List, Optional

from pash_annotations.util_flag_option import make_arg_simple
from pash_annotations.datatypes.basic_datatypes import (
    FlagOption,
    Operand,
    FileName,
    Flag,
)
from pash_annotations.datatypes.basic_datatypes_with_io import (
    make_stdout_with_access_output,
    make_stdin_with_access_stream_input,
)
from pash_annotations.datatypes.command_invocation_initial import (
    CommandInvocationInitial,
)
from pash_annotations.datatypes.command_invocation_prefix import CommandInvocationPrefix
from pash_annotations.datatypes.command_invocation_with_io import (
    CommandInvocationWithIO,
)
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
    make_splitter_consec_chunks,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.mapper_spec import (
    make_mapper_spec_seq,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.transformer_flag_option_list import (
    TransformerFlagOptionListFilter,
    TransformerFlagOptionListAdd,
    ChainTransformerFlagOptionList,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.aggregator_spec import (
    make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers,
)

import pash_annotations.annotation_generation.annotation_generation as AnnotationGeneration


cmd_name = "sort"

# TODO: with -m, we could do a reduction tree


def test_sort_1() -> None:
    args: List[FlagOption] = []
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
    assert para_info is not None and len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # only check splitter and actual mappers and aggregators
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    # check that results of getting mapper and aggregator are fine
    goal_mapper_spec = make_mapper_spec_seq()
    # TODO: change to actual check whether it does what is is supposed to do
    flag_option_list_to_keep = [
        "-b",
        "-d",
        "-f",
        "-g",
        "-i",
        "-M",
        "-h",
        "-n",
        "-r",
        "--sort",
        "-V",
        "-k",
        "-t",
    ]
    transformer_flag_option_list_filter: TransformerFlagOptionListFilter = (
        TransformerFlagOptionListFilter(flag_option_list_to_keep)
    )
    transformer_flag_option_list_add: TransformerFlagOptionListAdd = (
        TransformerFlagOptionListAdd([Flag("-m")])
    )
    chain_transformer_flag_option_list: ChainTransformerFlagOptionList = (
        ChainTransformerFlagOptionList(
            [transformer_flag_option_list_filter, transformer_flag_option_list_add]
        )
    )
    goal_aggregator_spec = (
        make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(
            flag_option_list_transformer=chain_transformer_flag_option_list,
            is_implemented=True,
        )
    )
    assert parallelizer1.get_mapper_spec() == goal_mapper_spec
    assert parallelizer1.get_aggregator_spec() == goal_aggregator_spec


def test_sort_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-b"]), make_arg_simple(["-f"])]
    operands: List[Operand] = []
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
    assert para_info is not None and len(para_info.parallelizer_list) == 1
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    # only check splitter and actual mappers and aggregators
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    # check that results of getting mapper and aggregator are fine
    # TODO: change to actual check whether it does what is is supposed to do: with flag option list


def test_sort_3() -> None:
    args: List[FlagOption] = [
        make_arg_simple(["-s"]),
        make_arg_simple(["-o", FileName("output.txt")]),
    ]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
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
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert (
        cmd_inv_with_io.implicit_use_of_streaming_input
        == make_stdin_with_access_stream_input()
    )
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert (
        para_info is not None and len(para_info.parallelizer_list) == 0
    )  # because of stable sort


def test_sort_5() -> None:
    args: List[FlagOption] = [make_arg_simple(["-m"])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
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
    assert (
        para_info is not None and len(para_info.parallelizer_list) == 0
    )  # because of stable sort


def test_sort_6() -> None:
    args: List[FlagOption] = [make_arg_simple(["--files0-from", FileName("input.txt")])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
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
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
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
    assert (
        para_info is not None and len(para_info.parallelizer_list) == 0
    )  # because of files0-from
