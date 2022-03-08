from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand
from parallelizers.ParallelizerIndivFiles import ParallelizerIndivFiles
from parallelizers.ParallelizerRoundRobin import ParallelizerRoundRobin

import AnnotationGeneration

cmd_name = "grep"


def test_grep_1():
    args = [make_arg_simple(["-c"]), make_arg_simple(["-L"]), make_arg_simple(["-f", "dict.txt"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[0])
    assert ParallelizerRoundRobin.is_parallelizer_mapper_seq_aggregator_cus2(meta.get_parallelizer_list()[1], "merge_keeping_longer_output")


def test_grep_2():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-b"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[0])
    assert ParallelizerRoundRobin.is_parallelizer_mapper_custom_aggregator_conc(meta.get_parallelizer_list()[1], "add_byte_offset")


def test_grep_3():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"])]
    operands = [Operand("in1.txt"),
                Operand("-")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[0])
    assert ParallelizerRoundRobin.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[1])


def test_grep_4():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"]),
            make_arg_simple(["-n"]), make_arg_simple(["-b"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    assert ParallelizerIndivFiles.is_parallelizer_mapper_seq_aggregator_conc(meta.get_parallelizer_list()[0])
    assert ParallelizerRoundRobin.is_parallelizer_mapper_custom_aggregator_conc(meta.get_parallelizer_list()[1],
                                                                                "add_line_number_and_byte_offset")


def test_grep_5():
    args = [make_arg_simple(["-q"]), make_arg_simple(["-s"])]
    operands = [Operand("*"),
                Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 0

    assert len(meta.get_parallelizer_list()) == 0


def test_grep_6():
    args = []
    operands = [Operand("*")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1  # only stdin
    assert len(meta.get_output_list()) == 2

# TODO: add each one test case where only stdout and stderr is used (similar to 5)
