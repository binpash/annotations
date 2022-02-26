from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand

import AnnotationGeneration

cmd_name = "tr"

# commands taken from spell script in one-liners


def test_tr_1():
    args = [make_arg_simple(["-c"]), make_arg_simple(["-s"])]
    operands = [Operand("A-Za-z"),
                Operand("\\n")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 1


def test_tr_2():
    args = []
    operands = [Operand("A-Z"),
                Operand("a-z")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 1


def test_tr_3():
    args = [make_arg_simple(["-d"])]
    operands = [Operand("'[:punct:]'")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 1

