from datatypes.Arg import make_arg_simple
from datatypes.Operand import Operand
from annotation_generation.parallelizers.Parallelizer import Parallelizer

import annotation_generation.AnnotationGeneration as AnnotationGeneration

cmd_name = "cut"

# commands taken from spell script in one-liners


def test_cut_1() -> None:
    args = []
    operands = [Operand("in1.txt"),
                Operand("in2.txt")]

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 2
    assert len(meta.get_output_list()) == 2     # stdout and stderr

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin()


def test_cut_2() -> None:
    args = [make_arg_simple(["-z"])]
    operands = []

    meta = AnnotationGeneration.get_meta_from_cmd_invocation(cmd_name, args, operands)

    assert len(meta.get_input_list()) == 1  # i.e. stdin
    assert len(meta.get_output_list()) == 2

    assert len(meta.get_parallelizer_list()) == 2
    [parallelizer1, parallelizer2] = meta.get_parallelizer_list()
    assert parallelizer1 == Parallelizer.make_parallelizer_indiv_files()
    assert parallelizer2 == Parallelizer.make_parallelizer_round_robin()
