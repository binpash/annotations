import pytest
from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand
from parser.parser import parse_json


# TODO: fix the warning about 'invalid escape sequence '\s''
# @pytest.mark.skip(reason="we want the main branch not to have failing test cases")
# TODO: change to new datatype for command invocation
def test_grep_1():
    parser_result_list = parse_json("grep -e '^\s*def ' -m 3 -n test.py", "grep.json")

    args = [make_arg_simple(["-e", "'^\s*def '"]), make_arg_simple(["-m", "3"])]
    operands = [Operand("test.py")]
    expected_result = ["grep", args, operands]

    assert expected_result == parser_result_list
