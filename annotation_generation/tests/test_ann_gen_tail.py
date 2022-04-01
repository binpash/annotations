from util import make_arg_simple
from datatypes.Operand import Operand
from annotation_generation.datatypes.parallelizability.Parallelizer import Parallelizer

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "tail"


def test_tail_1() -> None:
    args = [make_arg_simple(["-q"])]
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2     # stdout and stderr

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()


def test_tail_2() -> None:
    args = [make_arg_simple(["--version"])]
    operands = [Operand("in1.txt"),
                Operand("-"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 3
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 1
    [parallelizer1] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
