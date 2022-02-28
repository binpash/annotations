from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand

import AnnotationGeneration

cmd_name = "grep"


def test_grep_1():
    args = [make_arg_simple(["-f", "dict.txt"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2


def test_grep_2():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2


def test_grep_3():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"])]
    operands = [Operand("in1.txt"),
                Operand("-")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 2


def test_grep_4():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 2


def test_grep_5():
    args = [make_arg_simple(["-q"]), make_arg_simple(["-s"])]
    operands = [Operand("*"),
                Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 0


def test_grep_6():
    args = []
    operands = [Operand("*")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1  # only stdin
    assert len(meta.get_output_list()) == 2

# TODO: add each one test case where only stdout and stderr is used (similar to 5)