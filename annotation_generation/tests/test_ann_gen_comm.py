from util import make_arg_simple
from datatypes.Operand import Operand

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "comm"


def test_comm_1() -> None:
    args = [make_arg_simple(["-12"])]
    operands = [Operand("tocomm1.txt"),
                Operand("tocomm2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2     # dest and stderr


def test_comm_2() -> None:
    args = []
    # illegal to have more than 2 files to compare
    operands = [Operand("tocomm1.txt"),
                Operand("tocomm2.txt"),
                Operand("tocomm3.txt")]

    try:
        _meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)
        assert False
    except Exception:
        assert True


def test_comm_3() -> None:
    args = [make_arg_simple(["--version"])]
    operands = []

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 0
    assert len(meta.get_output_list()) == 2     # stdout, stderr
