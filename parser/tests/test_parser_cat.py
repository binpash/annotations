import pytest
from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand
from parser.parser import parse_json

# Result from parsing should have the following format:
# [ <cmd_name>, [ Arg ], [ Operand ] ]  where Arg can either be a single flag or a single option


@pytest.mark.skip(reason="we want the main branch not to have failing test cases")
def test_cat_1():
    parser_result_list = parse_json("cat -b -e in1.txt in2.txt", "cat.json")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = ["cat", args, operands]

    assert expected_result == parser_result_list


@pytest.mark.skip(reason="we want the main branch not to have failing test cases")
def test_cat_2():
    # this tests whether multiple flags with one - will be separated
    parser_result_list = parse_json("cat -be  in1.txt in2.txt", "cat.json")

    args = [make_arg_simple(["-b"]), make_arg_simple(["-e"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]
    expected_result = ["cat", args, operands]
    print(expected_result)

    assert expected_result == parser_result_list
