from util_flag_option import make_arg_simple
from datatypes_new.BasicDatatypes import Operand, FileName
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from parser_new.parser import parse


def test_sort_1():
    parser_result = parse("sort in1.txt in2.txt")

    args = []
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = CommandInvocationInitial("sort", args, operands)

    assert expected_result == parser_result


def test_sort_2():
    parser_result = parse("sort -b -o result.txt in1.txt in2.txt")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-o", "result.txt"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = CommandInvocationInitial("sort", args, operands)

    assert expected_result == parser_result

def test_sort_3():
    # this tests whether options will be mapped to their primary representation
    parser_result = parse("sort -b --output result.txt in1.txt in2.txt")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-o", "result.txt"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = CommandInvocationInitial("sort", args, operands)

    assert expected_result == parser_result
