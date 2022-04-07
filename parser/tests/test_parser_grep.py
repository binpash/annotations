import pytest
from util_flag_option import make_arg_simple
from datatypes.BasicDatatypes import ArgStringType, Operand
from datatypes.CommandInvocation import CommandInvocation
from parser.parser import parse_json


# @pytest.mark.skip(reason="we want the main branch not to have failing test cases")
def test_grep_1():
    parser_result = parse_json(r"grep -e '^\s*def' -m 3 -n test.py", "grep.json")

    args = [make_arg_simple(["-e", ArgStringType(r"^\s*def")]),
            make_arg_simple(["-m", ArgStringType("3")]),
            # make_arg_simple(["-m", "3"]),
            make_arg_simple(["-n"])]
    operands = [Operand("test.py")]
    expected_result = CommandInvocation("grep", args, operands)

    assert expected_result == parser_result
