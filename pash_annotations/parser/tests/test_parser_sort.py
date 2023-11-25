from pash_annotations.util_flag_option  import make_arg_simple
from pash_annotations.datatypes.basic_datatypes import Operand
from pash_annotations.datatypes.command_invocation_initial import CommandInvocationInitial
from pash_annotations.parser.parser import parse


def test_sort_1():
    parser_result = parse("sort in1.txt in2.txt")

    args = []
    operands = [Operand("in1.txt"), Operand("in2.txt")]
    expected_result = CommandInvocationInitial("sort", args, operands)

    assert expected_result == parser_result


def test_sort_2():
    parser_result = parse("sort -b -o result.txt in1.txt in2.txt")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-o", "result.txt"])]
    operands = [Operand("in1.txt"), Operand("in2.txt")]
    expected_result = CommandInvocationInitial("sort", args, operands)

    assert expected_result == parser_result


def test_sort_3():
    # this tests whether options will be mapped to their primary representation
    parser_result = parse("sort -b --output result.txt in1.txt in2.txt")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-o", "result.txt"])]
    operands = [Operand("in1.txt"), Operand("in2.txt")]
    expected_result = CommandInvocationInitial("sort", args, operands)

    assert expected_result == parser_result
