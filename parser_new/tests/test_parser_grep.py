from util_flag_option import make_arg_simple
from datatypes_new.BasicDatatypes import ArgStringType, Operand
from datatypes_new.CommandInvocationInitial import CommandInvocationInitial
from parser_new.parser import parse


def test_grep_1():
    parser_result = parse(r"grep -e '^\s*def' -m 3 -n test.py")

    args = [make_arg_simple(["-e", r"^\s*def"]),
            make_arg_simple(["-m", "3"]),
            make_arg_simple(["-n"])]
    operands = [Operand("test.py")]
    expected_result = CommandInvocationInitial("grep", args, operands)

    assert expected_result == parser_result
