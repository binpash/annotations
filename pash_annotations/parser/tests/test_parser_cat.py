from pash_annotations.util_flag_option  import make_arg_simple
from pash_annotations.datatypes.basic_datatypes import Operand
from pash_annotations.datatypes.command_invocation_initial import CommandInvocationInitial
from pash_annotations.parser.parser import parse


def test_cat_1():
    parser_result = parse("cat -b -e in1.txt in2.txt")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
    operands = [Operand("in1.txt"), Operand("in2.txt")]
    expected_result = CommandInvocationInitial("cat", args, operands)

    assert expected_result == parser_result


def test_cat_2():
    # this tests whether multiple flags with one - will be separated
    parser_result = parse("cat -be  in1.txt in2.txt")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
    operands = [Operand("in1.txt"), Operand("in2.txt")]
    expected_result = CommandInvocationInitial("cat", args, operands)

    assert expected_result == parser_result
