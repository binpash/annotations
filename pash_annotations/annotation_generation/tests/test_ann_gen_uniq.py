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
    make_splitter_consec_chunks,
    make_splitter_round_robin,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.mapper_spec import (
    make_mapper_spec_seq,
)
from pash_annotations.annotation_generation.datatypes.parallelizability.aggregator_spec import (
    make_aggregator_spec_adj_lines_seq,
    make_aggregator_spec_adj_lines_func_from_string_representation,
)

from pash_annotations.annotation_generation.annotation_generation import AnnotationGenerator

cmd_name = "uniq"


def test_uniq_1() -> None:
    args: List[FlagOption] = [make_arg_simple(["-D"])]
    operands: List[Operand] = [Operand("in.txt"), Operand("out.txt")]

    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    # cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGenerator().get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGenerator().get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 0


def test_uniq_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-c"])]
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
    ] = AnnotationGenerator().get_input_output_info_from_cmd_invocation(cmd_inv)
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
    ] = AnnotationGenerator().get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert (
        parallelizer1.get_aggregator_spec()
        == make_aggregator_spec_adj_lines_func_from_string_representation(
            "PLACEHOLDER:uniq_merge_count_uniq", is_implemented=False
        )
    )
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert (
        parallelizer2.get_aggregator_spec()
        == make_aggregator_spec_adj_lines_func_from_string_representation(
            "PLACEHOLDER:uniq_merge_count_uniq", is_implemented=False
        )
    )


def test_uniq_3() -> None:
    args: List[FlagOption] = []
    operands: List[Operand] = [Operand("in.txt"), Operand("out.txt")]
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(
        cmd_name, flag_option_list=args, operand_list=operands
    )
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(
        cmd_inv.cmd_name, cmd_inv.flag_option_list, []
    )

    # IO Info
    io_info: Optional[
        InputOutputInfo
    ] = AnnotationGenerator().get_input_output_info_from_cmd_invocation(cmd_inv)
    assert io_info is not None
    cmd_inv_with_io: CommandInvocationWithIO = (
        io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    )
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 1
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 1
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: Optional[
        ParallelizabilityInfo
    ] = AnnotationGenerator().get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert para_info is not None and len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # check that specs for mapper and aggregator are fine
    assert parallelizer1.get_splitter() == make_splitter_consec_chunks()
    assert parallelizer1.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer1.get_aggregator_spec() == make_aggregator_spec_adj_lines_seq()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    assert parallelizer2.get_mapper_spec() == make_mapper_spec_seq()
    assert parallelizer2.get_aggregator_spec() == make_aggregator_spec_adj_lines_seq()
