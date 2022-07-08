from typing import List

from util_flag_option import make_arg_simple
from datatypes_new.BasicDatatypes import Flag, Option, FlagOption, Operand, FileName, ArgStringType
from datatypes_new.BasicDatatypesWithIO import make_stdout_with_access_output, make_stdin_with_access_stream_input
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from datatypes_new.CommandInvocationWithIO import CommandInvocationWithIO
from datatypes_new.CommandInvocationPrefix import CommandInvocationPrefix
from annotation_generation_new.datatypes.InputOutputInfo import InputOutputInfo
from annotation_generation_new.datatypes.ParallelizabilityInfo import ParallelizabilityInfo
from annotation_generation_new.datatypes.parallelizability.Parallelizer import Parallelizer
from annotation_generation_new.datatypes.parallelizability.Splitter import Splitter, make_splitter_indiv_files, \
    make_splitter_round_robin
from annotation_generation_new.datatypes.parallelizability.MapperSpec import make_mapper_spec_seq
from annotation_generation_new.datatypes.parallelizability.AggregatorSpec import \
    make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers
from annotation_generation_new.datatypes.parallelizability.TransformerFlagOptionList import\
    TransformerFlagOptionListFilter, TransformerFlagOptionListAdd, ChainTransformerFlagOptionList


import annotation_generation_new.AnnotationGeneration as AnnotationGeneration

cmd_name = "sort"

# TODO: with -m, we could do a reduction tree

def test_sort_1() -> None:
    args: List[FlagOption] = []
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
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # only check splitter and actual mappers and aggregators
    assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    # check that results of getting mapper and aggregator are fine
    goal_mapper_spec = make_mapper_spec_seq()
    # TODO: change to actual check whether it does what is is supposed to do
    flag_option_list_to_keep = [Flag("-b"), Flag("-d"), Flag("-f"), Flag("-g"), Flag("-i"), Flag("-M"), \
                                Flag("-h"), Flag("-n"), Flag("-r"), Option("--sort", ""), Flag("-V"), Flag("-k"),
                                Flag("-t")]
    transformer_flag_option_list_filter: TransformerFlagOptionListFilter = \
        TransformerFlagOptionListFilter(flag_option_list_to_keep)
    transformer_flag_option_list_add: TransformerFlagOptionListAdd = TransformerFlagOptionListAdd([Flag("-m")])
    chain_transformer_flag_option_list: ChainTransformerFlagOptionList = \
        ChainTransformerFlagOptionList([transformer_flag_option_list_filter, transformer_flag_option_list_add])
    goal_aggregator_spec = make_aggregator_spec_custom_2_ary_from_cmd_inv_with_transformers(
        flag_option_list_transformer=chain_transformer_flag_option_list, is_implemented=True)
    assert parallelizer1.get_mapper_spec() == goal_mapper_spec
    assert parallelizer1.get_aggregator_spec() == goal_aggregator_spec
    assert parallelizer2.get_mapper_spec() == goal_mapper_spec
    assert parallelizer2.get_aggregator_spec() == goal_aggregator_spec


def test_sort_2() -> None:
    args: List[FlagOption] = [make_arg_simple(["-b"]), make_arg_simple(["-f"])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)
    cmd_inv_pref: CommandInvocationPrefix = CommandInvocationPrefix(cmd_inv.cmd_name, cmd_inv.flag_option_list, [])

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 2
    parallelizer1: Parallelizer = para_info.parallelizer_list[0]
    parallelizer2: Parallelizer = para_info.parallelizer_list[1]
    # only check splitter and actual mappers and aggregators
    assert parallelizer1.get_splitter() == make_splitter_indiv_files()
    assert parallelizer2.get_splitter() == make_splitter_round_robin()
    # check that results of getting mapper and aggregator are fine
    # TODO: change to actual check whether it does what is is supposed to do: with flag option list

def test_sort_3() -> None:
    args: List[FlagOption] = [make_arg_simple(["-s"]),
            make_arg_simple(["-o", FileName("output.txt")])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output is None

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0 # because of stable sort

def test_sort_5() -> None:
    args: List[FlagOption] = [make_arg_simple(["-m"])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input == make_stdin_with_access_stream_input()
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0 # because of stable sort


def test_sort_6() -> None:
    args: List[FlagOption] = [make_arg_simple(["--files0-from", FileName("input.txt")])]
    operands: List[Operand] = []
    cmd_inv: CommandInvocationInitial = CommandInvocationInitial(cmd_name, flag_option_list=args, operand_list=operands)

    # IO Info
    io_info: InputOutputInfo = AnnotationGeneration.get_input_output_info_from_cmd_invocation(cmd_inv)
    cmd_inv_with_io: CommandInvocationWithIO = io_info.apply_input_output_info_to_command_invocation(cmd_inv)
    assert len(cmd_inv_with_io.get_operands_with_config_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_input()) == 0
    assert len(cmd_inv_with_io.get_operands_with_stream_output()) == 0
    assert cmd_inv_with_io.implicit_use_of_streaming_input is None
    assert cmd_inv_with_io.implicit_use_of_streaming_output == make_stdout_with_access_output()

    # Parallelizability Info
    para_info: ParallelizabilityInfo = AnnotationGeneration.get_parallelizability_info_from_cmd_invocation(cmd_inv)
    assert len(para_info.parallelizer_list) == 0 # because of files0-from
