from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand

import AnnotationGeneration

cmd_name = "uniq"

# commands taken from spell script in one-liners


def test_uniq_1():
    args = []
    operands = [Operand("in.txt"),
                Operand("out.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1
    assert len(meta.get_output_list()) == 2     # out and stderr


def test_uniq_2():
    args = [make_arg_simple(["-c"])]
    operands = []

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1  # i.e. stdin
    assert len(meta.get_output_list()) == 2  # stdout and stderr


def test_uniq_3():
    args = [make_arg_simple(["--help"])]
    operands = [Operand("in.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1  # we could do better here b/c of --help
    assert len(meta.get_output_list()) == 2  # stdout and stderr


def test_uniq_3():
    args = [make_arg_simple(["-s", "10"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt"),
                Operand("out.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2  # we could do better here
    assert len(meta.get_output_list()) == 2  # out and stderr

