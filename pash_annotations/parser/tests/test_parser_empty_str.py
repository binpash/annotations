'''This is solely to test whether commands with the empty string as an operand
such as echo "" function properly'''

from pash_annotations.datatypes.CommandInvocationInitial import CommandInvocationInitial
from pash_annotations.parser.parser import parse

def test_empty_str_1():
    parser_result = parse('echo ""')

    args = []
    operands = []
    expected_result = CommandInvocationInitial("echo", args, operands)

    assert expected_result == parser_result

def test_empty_str_2():
    parser_result = parse('cat ""')

    args = []
    operands = []
    expected_result = CommandInvocationInitial("cat", args, operands)

    assert expected_result == parser_result
