from util_flag_option import make_arg_simple
from datatypes.BasicDatatypes import Operand, FileName
from datatypes.CommandInvocation import CommandInvocation
from parser.parser import parse_json


def test_sort_1():
    parser_result = parse_json("sort in1.txt in2.txt", "sort.json")

    args = []
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = CommandInvocation("sort", args, operands)

    assert expected_result == parser_result


def test_sort_2():
    parser_result = parse_json("sort -b -o result.txt in1.txt in2.txt", "sort.json")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-o", FileName("result.txt")])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = CommandInvocation("sort", args, operands)

    assert expected_result == parser_result

def test_sort_3():
    # this tests whether options will be mapped to their primary representation
    parser_result = parse_json("sort -b --output result.txt in1.txt in2.txt", "sort.json")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-o", FileName("result.txt")])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = CommandInvocation("sort", args, operands)

    assert expected_result == parser_result
