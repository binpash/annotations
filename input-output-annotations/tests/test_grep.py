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
    assert len(meta.get_output_list()) == 1


def test_grep_2():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 1


def test_grep_3():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"])]
    operands = [Operand("in1.txt"),
                Operand("-")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 1


def test_grep_4():
    args = [make_arg_simple(["-f", "dict.txt"]), make_arg_simple(["-e", "*"]), make_arg_simple(["-f", "dict2.txt"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt"),
                Operand("dict.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 4
    assert len(meta.get_output_list()) == 1
