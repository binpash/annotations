import sys
sys.path.append('../input-output-annotations/datatypes')
from Arg import make_arg_simple
from Operand import Operand
from parser import parse_json


def test_grep_1():
    parser_result_list = parse_json("grep -e '^\s*def ' -m 3 -n test.py", "../command-flag-option-info/grep.json")

    args = [make_arg_simple(["-e", "'^\s*def '"]), make_arg_simple(["-m", "3"])]
    operands = [Operand("test.py")]
    expected_result = ["grep", args, operands]

    assert expected_result == parser_result_list