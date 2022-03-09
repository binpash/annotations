from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand
from annotation_generation.parallelizers.Parallelizer import Parallelizer
from annotation_generation.parallelizers.Mapper import Mapper
from annotation_generation.parallelizers.Aggregator import Aggregator

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "grep"


def test_grep_1():
    args = [make_arg_simple(["-c"]), make_arg_simple(["-L"]), make_arg_simple(["-f", "dict.txt"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(aggregator=Aggregator.make_aggregator_custom_2_ary("merge_keeping_longer_output"))


def test_grep_2():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-b"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(mapper=Mapper.make_mapper_custom("add_byte_offset"))


def test_grep_3():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"])]
    operands = [Operand("in1.txt"),
                Operand("-")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin()


def test_grep_4():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"]),
            make_arg_simple(["-n"]), make_arg_simple(["-b"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin(mapper=Mapper.make_mapper_custom("add_line_number_and_byte_offset"))


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
