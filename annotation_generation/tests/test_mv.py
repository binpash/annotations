from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand

import AnnotationGeneration

cmd_name = "mv"


def test_mv_1():
    args = [make_arg_simple(["-t", "dest"])]
    operands = [Operand("tomove1.txt"),
                Operand("tomove2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2     # dest and stderr

    assert len(meta.get_parallelizer_list()) == 0


def test_mv_2():
    args = [make_arg_simple(["-v"])]
    operands = [Operand("tomove1.txt"),
                Operand("tomove2.txt"),
                Operand("dest.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2     # dest and stderr

    assert len(meta.get_parallelizer_list()) == 0


def test_mv_3():
    args = [make_arg_simple(["-t", "dest1.txt"]),
            make_arg_simple(["-t", "dest2.txt"])]
    # illegal to have -t twice
    operands = [Operand("tomove1.txt"),
                Operand("tomove2.txt"),
                Operand("dest.txt")]

    try:
        _meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)
        assert False
    except Exception:
        assert True


def test_mv_4():
    args = [make_arg_simple(["--version"])]
    operands = []

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 0
    assert len(meta.get_output_list()) == 2     # stdout, stderr

    assert len(meta.get_parallelizer_list()) == 0
